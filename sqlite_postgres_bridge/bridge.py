"""
Main bridge module that implements the SQLite virtual table interface
to connect to PostgreSQL databases.
"""

import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor
import logging
from typing import Optional, Dict, Any, List
import os

from .connection_manager import ConnectionManager
from .query_translator import QueryTranslator
from .data_mapper import DataMapper
from .virtual_table_interface import VirtualTableInterface

class SQLitePostgreSQLBridge:
    """
    Main bridge class that connects SQLite to PostgreSQL.
    Implements SQLite virtual table interface for transparent access.
    """
    
    def __init__(self, sqlite_conn: sqlite3.Connection, 
                 postgres_url: str, 
                 connection_pool_size: int = 5):
        """
        Initialize the bridge with SQLite connection and PostgreSQL URL.
        
        Args:
            sqlite_conn: Active SQLite connection
            postgres_url: PostgreSQL connection string
            connection_pool_size: Number of connections to maintain
        """
        self.sqlite_conn = sqlite_conn
        self.postgres_url = postgres_url
        self.connection_pool_size = connection_pool_size
        
        # Initialize components
        self.connection_manager = ConnectionManager(
            postgres_url, 
            connection_pool_size
        )
        self.query_translator = QueryTranslator()
        self.data_mapper = DataMapper()
        self.virtual_table_interface = VirtualTableInterface(
            sqlite_conn, 
            postgres_url
        )
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        self.logger.info("SQLite to PostgreSQL bridge initialized")
        
    def initialize(self) -> bool:
        """
        Initialize the bridge and establish connections.
        Create virtual tables that redirect to PostgreSQL.
        
        Returns:
            True if initialization successful, False otherwise
        """
        try:
            # Test PostgreSQL connection
            pg_conn = self.connection_manager.get_connection()
            
            # Create virtual tables that redirect all operations to PostgreSQL
            from .sqlite_vtab import activate_bridge
            
            # Get SQLite database path
            sqlite_path = self.sqlite_conn.execute("PRAGMA database_list").fetchone()[2]
            
            # Activate the bridge with virtual tables
            success = activate_bridge(sqlite_path, self.postgres_url)
            
            if success:
                self.logger.info("Bridge initialized successfully with virtual tables")
            else:
                self.logger.error("Failed to initialize virtual tables")
                
            return success
            
        except Exception as e:
            self.logger.error(f"Bridge initialization failed: {str(e)}")
            return False
            
    def _migrate_schema(self) -> None:
        """Migrate schema from SQLite to PostgreSQL."""
        try:
            # Get SQLite schema
            sqlite_cursor = self.sqlite_conn.cursor()
            sqlite_cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
            tables = sqlite_cursor.fetchall()
            
            if not tables:
                self.logger.info("No tables found in SQLite database")
                return
                
            # Get PostgreSQL connection directly
            import psycopg2
            pg_conn = psycopg2.connect(self.postgres_url)
            pg_cursor = pg_conn.cursor()
            
            for (sql,) in tables:
                if sql:
                    # Convert SQLite CREATE TABLE to PostgreSQL
                    pg_sql = self._convert_sqlite_to_postgres(sql)
                    if pg_sql:
                        try:
                            pg_cursor.execute(pg_sql)
                            pg_conn.commit()
                            self.logger.info(f"Created table from: {sql[:50]}...")
                        except Exception as e:
                            if "already exists" in str(e):
                                self.logger.debug(f"Table already exists: {str(e)}")
                            else:
                                self.logger.warning(f"Failed to create table: {str(e)}")
                                
            pg_conn.close()
            self.logger.info("Schema migration completed")
            
        except Exception as e:
            self.logger.error(f"Schema migration failed: {str(e)}")
            
    def _convert_sqlite_to_postgres(self, sqlite_sql: str) -> str:
        """Convert SQLite CREATE TABLE statement to PostgreSQL."""
        if not sqlite_sql or not sqlite_sql.strip():
            return ""
            
        try:
            # Basic validation
            if not sqlite_sql.upper().startswith("CREATE TABLE"):
                self.logger.warning(f"Skipping non-CREATE TABLE statement: {sqlite_sql[:50]}")
                return ""
                
            pg_sql = sqlite_sql
            
            # Basic type conversions
            pg_sql = pg_sql.replace("INTEGER PRIMARY KEY AUTOINCREMENT", "SERIAL PRIMARY KEY")
            pg_sql = pg_sql.replace("INTEGER PRIMARY KEY", "SERIAL PRIMARY KEY") 
            pg_sql = pg_sql.replace("AUTOINCREMENT", "")
            pg_sql = pg_sql.replace("BLOB", "BYTEA")
            
            # Add IF NOT EXISTS if not present
            if "IF NOT EXISTS" not in pg_sql.upper():
                pg_sql = pg_sql.replace("CREATE TABLE", "CREATE TABLE IF NOT EXISTS", 1)
                
            # Validate the result
            if not pg_sql.strip().endswith(";") and not pg_sql.strip().endswith(")"):
                pg_sql = pg_sql.rstrip() + ";"
                
            return pg_sql
            
        except Exception as e:
            self.logger.error(f"Failed to convert SQL: {sqlite_sql[:50]}... Error: {str(e)}")
            return ""
        
    def create_virtual_table(self, table_name: str, 
                              postgres_schema: Optional[Dict[str, Any]] = None) -> bool:
        """
        Create a virtual table that maps to a PostgreSQL table.
        
        Args:
            table_name: Name of the SQLite virtual table
            postgres_schema: PostgreSQL table schema definition
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create virtual table in interface
            result = self.virtual_table_interface.create_virtual_table(
                table_name, 
                postgres_schema
            )
            
            self.logger.info(f"Virtual table '{table_name}' created successfully")
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to create virtual table '{table_name}': {str(e)}")
            return False
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:  
        """
        Execute a query against the PostgreSQL backend.
        Intercept CREATE TABLE statements to replicate to PostgreSQL.
        
        Args:
            query: SQL query to execute
            params: Query parameters
            
        Returns:
            List of results from the query
        """
        # Intercept CREATE TABLE statements
        if query.strip().upper().startswith('CREATE TABLE'):
            self._replicate_table_to_postgres(query)
            
        return self.virtual_table_interface.execute_query(query, params)
        
    def execute_dml(self, query: str, params: tuple = ()) -> int:
        """
        Execute Data Manipulation Language operations (INSERT, UPDATE, DELETE).
        Intercept CREATE TABLE statements to replicate to PostgreSQL.
        
        Args:
            query: SQL DML query to execute
            params: Query parameters
            
        Returns:
            Number of affected rows
        """
        # Intercept CREATE TABLE statements
        if query.strip().upper().startswith('CREATE TABLE'):
            self._replicate_table_to_postgres(query)
            
        return self.virtual_table_interface.execute_dml(query, params)
        
    def _replicate_table_to_postgres(self, sqlite_sql: str) -> None:
        """Replicate a CREATE TABLE statement to PostgreSQL."""
        try:
            # Convert SQLite CREATE TABLE to PostgreSQL
            pg_sql = self._convert_sqlite_to_postgres(sqlite_sql)
            if not pg_sql:
                return
                
            # Execute on PostgreSQL
            import psycopg2
            pg_conn = psycopg2.connect(self.postgres_url)
            pg_cursor = pg_conn.cursor()
            
            pg_cursor.execute(pg_sql)
            pg_conn.commit()
            pg_conn.close()
            
            self.logger.info(f"Replicated table to PostgreSQL: {sqlite_sql[:50]}...")
            
        except Exception as e:
            if "already exists" in str(e):
                self.logger.debug(f"Table already exists in PostgreSQL: {str(e)}")
            else:
                self.logger.warning(f"Failed to replicate table to PostgreSQL: {str(e)}")
        
    def get_table_info(self, table_name: str) -> Dict[str, Any]:
        """
        Get comprehensive information about a table.
        
        Args:
            table_name: Name of the virtual table
            
        Returns:
            Dictionary with table information
        """
        return self.virtual_table_interface.get_table_info(table_name)
        
    def close(self) -> None:
        """Close all connections and clean up resources."""
        try:
            self.connection_manager.close()
            self.virtual_table_interface.close()
            self.logger.info("Bridge closed successfully")
        except Exception as e:
            self.logger.error(f"Error closing bridge: {str(e)}")
            
    def __enter__(self):
        """Context manager entry."""
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

# Example usage for testing
if __name__ == "__main__":
    # This would be used for testing purposes
    pass
