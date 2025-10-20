"""
Connection manager for PostgreSQL connections.
Handles connection pooling and management.
"""

import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
import logging
from contextlib import contextmanager
from typing import Optional

class ConnectionManager:
    """
    Manages PostgreSQL connections with connection pooling.
    """
    
    def __init__(self, connection_string: str, pool_size: int = 5):
        """
        Initialize the connection manager.
        
        Args:
            connection_string: PostgreSQL connection string
            pool_size: Size of the connection pool
        """
        self.connection_string = connection_string
        self.pool_size = pool_size
        self.connection_pool = None
        self.logger = logging.getLogger(__name__)
        
        # Create connection pool
        self._create_pool()
        
    def _create_pool(self) -> None:
        """
        Create a connection pool for PostgreSQL connections.
        """
        try:
            self.connection_pool = psycopg2.pool.ThreadedConnectionPool(
                minconn=1,
                maxconn=self.pool_size,
                dsn=self.connection_string
            )
            self.logger.info(f"Connection pool created with size {self.pool_size}")
            
        except Exception as e:
            self.logger.error(f"Failed to create connection pool: {str(e)}")
            raise
            
    @contextmanager
    def get_connection(self):
        """
        Context manager for getting a connection from the pool.
        
        Yields:
            PostgreSQL connection object
        """
        conn = None
        try:
            # Get connection from pool
            conn = self.connection_pool.getconn()
            yield conn
            
        except Exception as e:
            if conn:
                conn.rollback()
            self.logger.error(f"Error in connection context: {str(e)}")
            raise
            
        finally:
            # Return connection to pool
            if conn:
                self.connection_pool.putconn(conn)
                
    def close(self) -> None:
        """
        Close all connections in the pool.
        """
        if self.connection_pool:
            self.connection_pool.closeall()
            self.logger.info("Connection pool closed successfully")
            
    def test_connection(self) -> bool:
        """
        Test if the connection to PostgreSQL is working.
        
        Returns:
            True if connection is successful, False otherwise
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                cursor.close()
            return True
            
        except Exception as e:
            self.logger.error(f"Connection test failed: {str(e)}")
            return False
