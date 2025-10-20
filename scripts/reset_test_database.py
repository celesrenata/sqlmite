#!/usr/bin/env python3
"""
Script to reset the test database to a known state before running tests.
This ensures test isolation and prevents data contamination.
"""

import psycopg2
import logging
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def reset_test_database(
    host: str = "10.1.1.12",
    port: int = 5432,
    database: str = "testdb",
    username: str = "celes",
    password: str = "PSCh4ng3me!"
) -> bool:
    """
    Reset the test database to a known initial state.
    
    Args:
        host: PostgreSQL host
        port: PostgreSQL port
        database: Database name
        username: Database username
        password: Database password
        
    Returns:
        True if reset successful, False otherwise
    """
    connection = None
    try:
        logger.info("Connecting to test database for reset...")
        
        # Connect to the database
        connection = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=username,
            password=password
        )
        
        cursor = connection.cursor()
        
        # Drop existing test tables (if any)
        logger.info("Dropping existing test tables...")
        cursor.execute("""
            DROP TABLE IF EXISTS users CASCADE;
            DROP TABLE IF EXISTS products CASCADE;
            DROP TABLE IF EXISTS orders CASCADE;
        """)
        
        # Create fresh test tables
        logger.info("Creating fresh test tables...")
        
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Create products table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                price DECIMAL(10,2),
                category VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Create orders table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                product_id INTEGER REFERENCES products(id),
                quantity INTEGER NOT NULL,
                order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Insert initial test data
        logger.info("Inserting initial test data...")
        
        # Insert users
        cursor.execute("""
            INSERT INTO users (name, email) VALUES 
                ('John Doe', 'john@example.com'),
                ('Jane Smith', 'jane@example.com'),
                ('Bob Johnson', 'bob@example.com')
        """)
        
        # Insert products
        cursor.execute("""
            INSERT INTO products (name, price, category) VALUES 
                ('Laptop', 999.99, 'Electronics'),
                ('Book', 19.99, 'Education'),
                ('Coffee Mug', 12.50, 'Kitchen')
        """)
        
        # Commit all changes
        connection.commit()
        logger.info("Database reset completed successfully")
        
        return True
        
    except Exception as e:
        logger.error(f"Error resetting database: {str(e)}")
        if connection:
            connection.rollback()
        return False
        
    finally:
        if connection:
            connection.close()

def main():
    """Main function to run the database reset."""
    logger.info("Starting database reset process...")
    
    success = reset_test_database()
    
    if success:
        logger.info("Database reset completed successfully!")
        return 0
    else:
        logger.error("Database reset failed!")
        return 1

if __name__ == "__main__":
    exit(main())
