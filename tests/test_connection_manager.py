"""
Tests for the connection manager component.
"""

import unittest
from unittest.mock import Mock, patch
from sqlite_postgres_bridge.connection_manager import ConnectionManager

class TestConnectionManager(unittest.TestCase):
    """
    Test cases for the connection manager.
    """
    
    def setUp(self):
        """
        Set up test fixtures before each test method.
        """
        self.postgres_url = "postgresql://user:pass@localhost:5432/testdb"
        self.connection_pool_size = 5
        
        # Create a mock connection pool for testing
        self.mock_pool = Mock()
        
    def test_connection_manager_initialization(self):
        """
        Test that the connection manager initializes correctly.
        """
        # This test is mostly for ensuring no exceptions during initialization
        # Since we're mocking the pool, we can't fully test the real pool creation
        manager = ConnectionManager(self.postgres_url, self.connection_pool_size)
        self.assertIsNotNone(manager)
        
    def test_get_connection_context_manager(self):
        """
        Test getting a connection using the context manager.
        """
        # Mock the pool's getconn and putconn methods
        with patch('sqlite_postgres_bridge.connection_manager.psycopg2.pool.ThreadedConnectionPool') as mock_pool:
            # Setup mock pool
            mock_connection = Mock()
            mock_pool_instance = Mock()
            mock_pool_instance.getconn.return_value = mock_connection
            mock_pool_instance.putconn = Mock()
            mock_pool.return_value = mock_pool_instance
            
            manager = ConnectionManager(self.postgres_url, self.connection_pool_size)
            
            # Test the context manager
            with manager.get_connection() as conn:
                self.assertEqual(conn, mock_connection)
                
    def test_close_connection_pool(self):
        """
        Test closing the connection pool.
        """
        # Mock the pool
        with patch('sqlite_postgres_bridge.connection_manager.psycopg2.pool.ThreadedConnectionPool') as mock_pool:
            mock_pool_instance = Mock()
            mock_pool.return_value = mock_pool_instance
            
            manager = ConnectionManager(self.postgres_url, self.connection_pool_size)
            manager.close()
            
            # Verify closeall was called
            mock_pool_instance.closeall.assert_called_once()
            
    def test_test_connection(self):
        """
        Test connection testing functionality.
        """
        # Mock the pool and connection
        with patch('sqlite_postgres_bridge.connection_manager.psycopg2.pool.ThreadedConnectionPool') as mock_pool:
            mock_pool_instance = Mock()
            mock_pool.return_value = mock_pool_instance
            
            manager = ConnectionManager(self.postgres_url, self.connection_pool_size)
            
            # Test that it doesn't crash (actual implementation would need more complex mocking)
            result = manager.test_connection()
            # We can't fully test this without a real database connection
            
    def tearDown(self):
        """
        Clean up after each test method.
        """
        # Clean up any resources if needed
        pass

if __name__ == '__main__':
    unittest.main()
