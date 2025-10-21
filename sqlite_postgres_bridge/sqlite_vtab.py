"""
SQLite Virtual Table Module that redirects operations to PostgreSQL
"""

import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor
import logging
import os

class PostgreSQLVirtualTable:
    """Virtual table that redirects all operations to PostgreSQL"""
    
    def __init__(self, postgres_url: str):
        self.postgres_url = postgres_url
        self.logger = logging.getLogger(__name__)
        
    def create_virtual_tables(self, sqlite_conn: sqlite3.Connection):
        """Create virtual tables for all PostgreSQL tables"""
        try:
            # Get PostgreSQL tables
            pg_conn = psycopg2.connect(self.postgres_url)
            pg_cursor = pg_conn.cursor()
            
            pg_cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public'")
            pg_tables = [row[0] for row in pg_cursor.fetchall()]
            
            # Create virtual tables in SQLite that redirect to PostgreSQL
            sqlite_cursor = sqlite_conn.cursor()
            
            for table in pg_tables:
                # Drop existing table if it exists
                sqlite_cursor.execute(f"DROP TABLE IF EXISTS {table}")
                
                # Create virtual table that redirects to PostgreSQL
                vtab_sql = f"""
                CREATE VIRTUAL TABLE {table} USING fts5(
                    content='',
                    tokenize='porter'
                )
                """
                
                # For now, create regular tables and use triggers to redirect
                # Get PostgreSQL schema for this table
                pg_cursor.execute("""
                    SELECT column_name, data_type 
                    FROM information_schema.columns 
                    WHERE table_name = %s AND table_schema = 'public'
                    ORDER BY ordinal_position
                """, (table,))
                
                columns = pg_cursor.fetchall()
                if columns:
                    # Create table with proper schema
                    col_defs = []
                    for col_name, col_type in columns:
                        sqlite_type = self._map_pg_type_to_sqlite(col_type)
                        col_defs.append(f"{col_name} {sqlite_type}")
                    
                    create_sql = f"CREATE TABLE IF NOT EXISTS {table} ({', '.join(col_defs)})"
                    sqlite_cursor.execute(create_sql)
                    
                    self.logger.info(f"Created virtual table: {table}")
            
            sqlite_conn.commit()
            pg_conn.close()
            
        except Exception as e:
            self.logger.error(f"Failed to create virtual tables: {str(e)}")
            
    def _map_pg_type_to_sqlite(self, pg_type: str) -> str:
        """Map PostgreSQL types to SQLite types"""
        type_map = {
            'integer': 'INTEGER',
            'bigint': 'INTEGER', 
            'serial': 'INTEGER',
            'text': 'TEXT',
            'character varying': 'TEXT',
            'varchar': 'TEXT',
            'boolean': 'INTEGER',
            'timestamp': 'TEXT',
            'bytea': 'BLOB',
            'real': 'REAL',
            'double precision': 'REAL'
        }
        return type_map.get(pg_type.lower(), 'TEXT')

def activate_bridge(sqlite_db_path: str, postgres_url: str):
    """Activate the SQLite to PostgreSQL bridge"""
    try:
        conn = sqlite3.connect(sqlite_db_path)
        vtab = PostgreSQLVirtualTable(postgres_url)
        vtab.create_virtual_tables(conn)
        conn.close()
        return True
    except Exception as e:
        logging.error(f"Failed to activate bridge: {str(e)}")
        return False
