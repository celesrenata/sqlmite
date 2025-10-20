"""
Tests for the data mapper component.
"""

import unittest
from datetime import datetime, date
from sqlite_postgres_bridge.data_mapper import DataMapper

class TestDataMapper(unittest.TestCase):
    """
    Test cases for the data mapper.
    """
    
    def setUp(self):
        """
        Set up test fixtures before each test method.
        """
        self.mapper = DataMapper()
        
    def test_data_mapper_initialization(self):
        """
        Test that the data mapper initializes correctly.
        """
        self.assertIsNotNone(self.mapper)
        
    def test_map_results_empty(self):
        """
        Test mapping empty results.
        """
        results = []
        mapped_results = self.mapper.map_results(results)
        self.assertEqual(mapped_results, [])
        
    def test_map_results_single_row(self):
        """
        Test mapping a single row.
        """
        results = [{"id": 1, "name": "John", "created": datetime.now()}]
        mapped_results = self.mapper.map_results(results)
        self.assertEqual(len(mapped_results), 1)
        self.assertEqual(mapped_results[0]["id"], 1)
        self.assertEqual(mapped_results[0]["name"], "John")
        
    def test_map_results_multiple_rows(self):
        """
        Test mapping multiple rows.
        """
        results = [
            {"id": 1, "name": "John"},
            {"id": 2, "name": "Jane"}
        ]
        mapped_results = self.mapper.map_results(results)
        self.assertEqual(len(mapped_results), 2)
        self.assertEqual(mapped_results[0]["id"], 1)
        self.assertEqual(mapped_results[1]["id"], 2)
        
    def test_map_single_row(self):
        """
        Test mapping a single row.
        """
        row = {"id": 1, "name": "John"}
        mapped_row = self.mapper._map_row(row)
        self.assertEqual(mapped_row["id"], 1)
        self.assertEqual(mapped_row["name"], "John")
        
    def test_map_single_value(self):
        """
        Test mapping a single value.
        """
        # Test None value
        result = self.mapper._map_value(None)
        self.assertIsNone(result)
        
        # Test datetime value
        dt = datetime.now()
        result = self.mapper._map_value(dt)
        self.assertEqual(result, dt)
        
        # Test string value
        string_val = "test"
        result = self.mapper._map_value(string_val)
        self.assertEqual(result, string_val)
        
    def test_map_schema(self):
        """
        Test mapping a schema.
        """
        schema = {
            "id": {"type": "integer", "nullable": False},
            "name": {"type": "text", "nullable": True}
        }
        mapped_schema = self.mapper.map_schema(schema)
        self.assertEqual(len(mapped_schema), 2)
        self.assertIn("id", mapped_schema)
        self.assertIn("name", mapped_schema)
        
    def test_map_column(self):
        """
        Test mapping a column.
        """
        column_info = {"type": "integer", "nullable": False}
        mapped_column = self.mapper._map_column(column_info)
        self.assertEqual(mapped_column, column_info)
        
    def tearDown(self):
        """
        Clean up after each test method.
        """
        # Clean up any resources if needed
        pass

if __name__ == '__main__':
    unittest.main()
