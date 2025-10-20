"""
Main bridge module that implements the SQLite virtual table interface
to connect to PostgreSQL databases.
"""

import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor
import logging
from typing import Optional, Dict, Any

from .connection_manager import ConnectionManager
from .query_translator import QueryTranslator
from .data_mapper import DataMapper

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
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        self.logger.info("SQLite to PostgreSQL bridge initialized")
        
    def create_virtual_table(self, table_name: str, 
                              postgres_schema: Optional[Dict[str, Any]] = None) -> None:
        """
        Create a virtual table that maps to a PostgreSQL table.
        
        Args:
            table_name: Name of the SQLite virtual table
            postgres_schema: PostgreSQL table schema definition
        """
        # This would implement the SQLite virtual table interface
        # For now, we'll set up the connection and prepare for use
        self.logger.info(f"Creating virtual table {table_name}")
        
        # Store schema information for query translation
        if postgres_schema:
            self.postgres_schema = postgres_schema
            
    def execute_query(self, query: str, params: tuple = ()) -> list:
        """
        Execute a query against the PostgreSQL backend.
        
        Args:
            query: SQL query to execute
            params: Query parameters
            
        Returns:
            List of results from the query
        """
        try:
            # Translate SQLite query to PostgreSQL
            postgres_query = self.query_translator.translate(query)
            
            # Execute against PostgreSQL
            with self.connection_manager.get_connection() as conn:
                cursor = conn.cursor(cursor_factory=RealDictCursor)
                cursor.execute(postgres_query, params)
                results = cursor.fetchall()
                cursor.close()
                
                # Map results to SQLite format
                return self.data_mapper.map_results(results)
                
        except Exception as e:
            self.logger.error(f"Error executing query: {str(e)}")
            raise
            
    def execute_dml(self, query: str, params: tuple = ()) -> int:
        """
        Execute Data Manipulation Language operations (INSERT, UPDATE, DELETE).
        
        Args:
            query: SQL DML query to execute
            params: Query parameters
            
        Returns:
            Number of affected rows
        """
        try:
            # Translate SQLite query to PostgreSQL
            postgres_query = self.query_translator.translate(query)
            
            # Execute against PostgreSQL
            with self.connection_manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(postgres_query, params)
                affected_rows = cursor.rowcount
                conn.commit()
                cursor.close()
                
                return affected_rows
                
        except Exception as e:
            self.logger.error(f"Error executing DML: {str(e)}")
            raise
            
    def close(self) -> None:
        """Close all connections and clean up resources."""
        self.connection_manager.close()
        self.logger.info("Bridge closed successfully")
        
    def __enter__(self):
        """Context manager entry."""
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
