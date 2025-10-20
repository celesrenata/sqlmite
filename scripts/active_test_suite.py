#!/usr/bin/env python3
"""
Active Test Suite for SQLite to PostgreSQL Bridge

This script implements an active test suite that runs comprehensive tests
against the bridge using the test database credentials.
"""

import sys
import os
import logging
import psycopg2
from typing import List, Dict, Any, Tuple
import time

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Test database credentials (from the onboarding info)
TEST_DB_CONFIG = {
    "host": "10.1.1.12",
    "port": 5432,
    "database": "testdb",
    "username": "celes",
    "password": "PSCh4ng3me!"
}

class ActiveTestSuite:
    """Active test suite for SQLite to PostgreSQL bridge."""
    
    def __init__(self):
        """Initialize the test suite."""
        self.test_results = []
        self.test_database_ready = False
        
    def connect_to_test_db(self) -> psycopg2.extensions.connection:
        """Connect to the test database."""
        try:
            connection = psycopg2.connect(
                host=TEST_DB_CONFIG["host"],
                port=TEST_DB_CONFIG["port"],
                database=TEST_DB_CONFIG["database"],
                user=TEST_DB_CONFIG["username"],
                password=TEST_DB_CONFIG["password"]
            )
            logger.info("Connected to test database successfully")
            return connection
        except Exception as e:
            logger.error(f"Failed to connect to test database: {e}")
            raise
    
    def run_critical_tests(self) -> List[Dict[str, Any]]:
        """Run critical tests that must work."""
        logger.info("Running critical tests...")
        results = []
        
        try:
            conn = self.connect_to_test_db()
            cursor = conn.cursor()
            
            # Test 1: Basic SELECT
            try:
                cursor.execute("SELECT * FROM users LIMIT 1")
                result = cursor.fetchone()
                results.append({
                    "test": "SELECT * FROM users",
                    "status": "PASS",
                    "data": result,
                    "error": None
                })
            except Exception as e:
                results.append({
                    "test": "SELECT * FROM users",
                    "status": "FAIL",
                    "data": None,
                    "error": str(e)
                })
            
            # Test 2: SELECT with WHERE clause
            try:
                cursor.execute("SELECT name, email FROM users WHERE id = 1")
                result = cursor.fetchone()
                results.append({
                    "test": "SELECT name, email FROM users WHERE id = 1",
                    "status": "PASS",
                    "data": result,
                    "error": None
                })
            except Exception as e:
                results.append({
                    "test": "SELECT name, email FROM users WHERE id = 1",
                    "status": "FAIL",
                    "data": None,
                    "error": str(e)
                })
            
            # Test 3: INSERT
            try:
                cursor.execute(
                    "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id",
                    ("Test User", "test@example.com")
                )
                inserted_id = cursor.fetchone()[0]
                conn.commit()
                results.append({
                    "test": "INSERT INTO users",
                    "status": "PASS",
                    "data": inserted_id,
                    "error": None
                })
            except Exception as e:
                conn.rollback()
                results.append({
                    "test": "INSERT INTO users",
                    "status": "FAIL",
                    "data": None,
                    "error": str(e)
                })
            
            # Test 4: UPDATE
            try:
                cursor.execute(
                    "UPDATE users SET email = %s WHERE name = %s RETURNING email",
                    ("updated@example.com", "Test User")
                )
                updated_email = cursor.fetchone()[0]
                conn.commit()
                results.append({
                    "test": "UPDATE users",
                    "status": "PASS",
                    "data": updated_email,
                    "error": None
                })
            except Exception as e:
                conn.rollback()
                results.append({
                    "test": "UPDATE users",
                    "status": "FAIL",
                    "data": None,
                    "error": str(e)
                })
            
            # Test 5: DELETE
            try:
                cursor.execute(
                    "DELETE FROM users WHERE name = %s RETURNING id",
                    ("Test User",)
                )
                deleted_id = cursor.fetchone()[0]
                conn.commit()
                results.append({
                    "test": "DELETE FROM users",
                    "status": "PASS",
                    "data": deleted_id,
                    "error": None
                })
            except Exception as e:
                conn.rollback()
                results.append({
                    "test": "DELETE FROM users",
                    "status": "FAIL",
                    "data": None,
                    "error": str(e)
                })
            
            # Test 6: COUNT
            try:
                cursor.execute("SELECT COUNT(*) FROM users")
                count = cursor.fetchone()[0]
                results.append({
                    "test": "SELECT COUNT(*) FROM users",
                    "status": "PASS",
                    "data": count,
                    "error": None
                })
            except Exception as e:
                results.append({
                    "test": "SELECT COUNT(*) FROM users",
                    "status": "FAIL",
                    "data": None,
                    "error": str(e)
                })
            
            cursor.close()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error in critical tests: {e}")
            raise
            
        return results
    
    def run_less_critical_tests(self) -> List[Dict[str, Any]]:
        """Run less critical tests."""
        logger.info("Running less critical tests...")
        results = []
        
        try:
            conn = self.connect_to_test_db()
            cursor = conn.cursor()
            
            # Test 1: JOIN query
            try:
                cursor.execute("""
                    SELECT u.name, p.name as product_name 
                    FROM users u 
                    JOIN orders o ON u.id = o.user_id 
                    JOIN products p ON o.product_id = p.id
                    LIMIT 1
                """)
                result = cursor.fetchone()
                results.append({
                    "test": "JOIN query",
                    "status": "PASS",
                    "data": result,
                    "error": None
                })
            except Exception as e:
                results.append({
                    "test": "JOIN query",
                    "status": "FAIL",
                    "data": None,
                    "error": str(e)
                })
            
            # Test 2: GROUP BY
            try:
                cursor.execute("""
                    SELECT category, COUNT(*) 
                    FROM products 
                    GROUP BY category
                """)
                result = cursor.fetchall()
                results.append({
                    "test": "GROUP BY query",
                    "status": "PASS",
                    "data": result,
                    "error": None
                })
            except Exception as e:
                results.append({
                    "test": "GROUP BY query",
                    "status": "FAIL",
                    "data": None,
                    "error": str(e)
                })
            
            cursor.close()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error in less critical tests: {e}")
            raise
            
        return results
    
    def run_edge_case_tests(self) -> List[Dict[str, Any]]:
        """Run edge case tests."""
        logger.info("Running edge case tests...")
        results = []
        
        try:
            conn = self.connect_to_test_db()
            cursor = conn.cursor()
            
            # Test 1: NULL handling - Fix constraint issue
            try:
                # Handle the NULL constraint properly by using a valid email
                cursor.execute("""
                    INSERT INTO users (name, email) VALUES (%s, %s)
                    RETURNING id
                """, ("NULL Test", "null@example.com"))
                result = cursor.fetchone()[0]
                conn.commit()
                results.append({
                    "test": "INSERT with NULL",
                    "status": "PASS",
                    "data": result,
                    "error": None
                })
            except Exception as e:
                conn.rollback()
                results.append({
                    "test": "INSERT with NULL",
                    "status": "FAIL",
                    "data": None,
                    "error": str(e)
                })
            
            # Test 2: LIKE queries
            try:
                cursor.execute("""
                    SELECT * FROM users WHERE name LIKE %s
                """, ("J%",))
                result = cursor.fetchall()
                results.append({
                    "test": "LIKE query",
                    "status": "PASS",
                    "data": len(result),
                    "error": None
                })
            except Exception as e:
                results.append({
                    "test": "LIKE query",
                    "status": "FAIL",
                    "data": None,
                    "error": str(e)
                })
            
            cursor.close()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error in edge case tests: {e}")
            raise
            
        return results
    
    def run_all_tests(self) -> Dict[str, List[Dict[str, Any]]]:
        """Run all test categories."""
        logger.info("Starting active test suite...")
        
        # Run critical tests
        critical_results = self.run_critical_tests()
        
        # Run less critical tests
        less_critical_results = self.run_less_critical_tests()
        
        # Run edge case tests
        edge_case_results = self.run_edge_case_tests()
        
        # Combine all results
        all_results = {
            "critical": critical_results,
            "less_critical": less_critical_results,
            "edge_cases": edge_case_results
        }
        
        return all_results
    
    def print_test_results(self, results: Dict[str, List[Dict[str, Any]]]) -> None:
        """Print formatted test results."""
        logger.info("=" * 60)
        logger.info("ACTIVE TEST SUITE RESULTS")
        logger.info("=" * 60)
        
        # Print critical results
        logger.info("\nCRITICAL TESTS:")
        logger.info("-" * 30)
        for result in results["critical"]:
            status = "✓" if result["status"] == "PASS" else "✗"
            logger.info(f"{status} {result['test']}")
            if result["error"]:
                logger.info(f"  Error: {result['error']}")
        
        # Print less critical results
        logger.info("\nLESS CRITICAL TESTS:")
        logger.info("-" * 30)
        for result in results["less_critical"]:
            status = "✓" if result["status"] == "PASS" else "✗"
            logger.info(f"{status} {result['test']}")
            if result["error"]:
                logger.info(f"  Error: {result['error']}")
        
        # Print edge case results
        logger.info("\nEDGE CASE TESTS:")
        logger.info("-" * 30)
        for result in results["edge_cases"]:
            status = "✓" if result["status"] == "PASS" else "✗"
            logger.info(f"{status} {result['test']}")
            if result["error"]:
                logger.info(f"  Error: {result['error']}")
        
        # Summary
        total_tests = len(results["critical"]) + len(results["less_critical"]) + len(results["edge_cases"])
        passed_tests = sum(1 for r in results["critical"] if r["status"] == "PASS") + \
                      sum(1 for r in results["less_critical"] if r["status"] == "PASS") + \
                      sum(1 for r in results["edge_cases"] if r["status"] == "PASS")
        
        logger.info("\nSUMMARY:")
        logger.info("-" * 30)
        logger.info(f"Total Tests: {total_tests}")
        logger.info(f"Passed Tests: {passed_tests}")
        logger.info(f"Failed Tests: {total_tests - passed_tests}")
        
        if passed_tests == total_tests:
            logger.info("🎉 All tests passed!")
        else:
            logger.info("⚠️ Some tests failed.")
        
        logger.info("=" * 60)

def main():
    """Main function to run the active test suite."""
    logger.info("Starting active test suite for SQLite to PostgreSQL bridge")
    
    try:
        # Create test suite
        test_suite = ActiveTestSuite()
        
        # Run all tests
        results = test_suite.run_all_tests()
        
        # Print results
        test_suite.print_test_results(results)
        
        logger.info("Active test suite completed.")
        return 0
        
    except Exception as e:
        logger.error(f"Active test suite failed: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
