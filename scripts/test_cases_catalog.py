"""
Test Cases Catalog for SQLite to PostgreSQL Bridge

This file catalogs all the test cases organized by priority level.
"""

# Critical Commands (Must Work)
CRITICAL_COMMANDS = [
    "Basic database connection and authentication",
    "SELECT * FROM users",
    "SELECT name, email FROM users WHERE id = 1",
    "INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com')",
    "UPDATE users SET email = 'updated@example.com' WHERE id = 1",
    "DELETE FROM users WHERE id = 3",
    "SELECT COUNT(*) FROM users",
    "SELECT * FROM users ORDER BY id DESC LIMIT 2",
    "SELECT COUNT(*) FROM products",
    "SELECT name, price FROM products WHERE price > 50"
]

# Less Critical Commands (Should Work)
LESS_CRITICAL_COMMANDS = [
    "SELECT u.name, p.name as product_name FROM users u JOIN orders o ON u.id = o.user_id JOIN products p ON o.product_id = p.id",
    "INSERT INTO products (name, price, category) VALUES ('Smartphone', 699.99, 'Electronics')",
    "UPDATE products SET price = 799.99 WHERE name = 'Laptop'",
    "SELECT p.name, p.price, u.name as user_name FROM products p JOIN orders o ON p.id = o.product_id JOIN users u ON o.user_id = u.id",
    "SELECT category, COUNT(*) FROM products GROUP BY category",
    "SELECT u.name, COUNT(o.id) as order_count FROM users u LEFT JOIN orders o ON u.id = o.user_id GROUP BY u.id, u.name",
    "SELECT * FROM users WHERE email LIKE '%example.com'",
    "SELECT * FROM products WHERE created_at >= '2023-01-01'",
    "SELECT u.name, p.name, o.quantity FROM users u JOIN orders o ON u.id = o.user_id JOIN products p ON o.product_id = p.id",
    "SELECT p.name, p.price, u.name as user_name FROM products p JOIN orders o ON p.id = o.product_id JOIN users u ON o.user_id = u.id WHERE p.price > 100"
]

# Edge Cases (Special Handling)
EDGE_CASES = [
    "SELECT * FROM users WHERE name IS NULL",
    "SELECT * FROM users WHERE name IS NOT NULL",
    "INSERT INTO users (name, email) VALUES ('Special Char Test', 'test@exa%mple.com')",
    "SELECT * FROM users WHERE email = 'john@example.com' AND name = 'John Doe'",
    "SELECT * FROM users WHERE email IN ('john@example.com', 'jane@example.com')",
    "SELECT * FROM users WHERE id BETWEEN 1 AND 2",
    "SELECT * FROM users WHERE created_at IS NULL",
    "INSERT INTO users (name, email) VALUES ('NULL Test', NULL)",
    "SELECT * FROM users WHERE name = ''",
    "SELECT * FROM users WHERE email = 'jane@example.com' AND email IS NOT NULL",
    "SELECT name, email FROM users WHERE name LIKE 'J%'",
    "SELECT name, email FROM users WHERE name LIKE '%n%'",
    "SELECT name, email FROM users WHERE name LIKE 'J_n%'",
    "SELECT * FROM users WHERE name = 'John Doe' OR name = 'Jane Smith'",
    "SELECT * FROM users WHERE name = 'John Doe' AND email = 'john@example.com' AND id = 1",
    "SELECT * FROM users WHERE id = 1 AND name = 'John Doe' AND email = 'john@example.com'",
    "SELECT * FROM users WHERE id IN (1, 2, 3) AND name LIKE 'J%'",
    "SELECT * FROM users WHERE id NOT IN (1, 2)",
    "SELECT * FROM users WHERE id != 1",
    "SELECT * FROM users WHERE name != 'John Doe'"
]

# Data Type Tests
DATA_TYPE_TESTS = [
    "SELECT * FROM products WHERE price = 999.99",
    "SELECT * FROM products WHERE price = 19.99",
    "SELECT * FROM products WHERE price = 12.50",
    "SELECT * FROM products WHERE price = 0.00",
    "SELECT * FROM users WHERE created_at IS NOT NULL",
    "SELECT * FROM products WHERE created_at IS NOT NULL",
    "SELECT * FROM orders WHERE quantity = 1",
    "SELECT * FROM orders WHERE quantity = 5",
    "SELECT * FROM orders WHERE quantity = 10"
]

# Error Handling Tests
ERROR_HANDLING_TESTS = [
    "SELECT * FROM non_existent_table",
    "INSERT INTO users (name, email) VALUES (NULL, 'test@example.com')",
    "INSERT INTO users (name, email) VALUES ('Test', NULL)",
    "INSERT INTO users (name, email) VALUES ('Test', 'invalid-email')",
    "UPDATE users SET email = NULL WHERE id = 1",
    "DELETE FROM users WHERE id = 999999",
    "SELECT * FROM users WHERE id = -1",
    "SELECT * FROM users WHERE id = 0",
    "INSERT INTO users (name, email) VALUES ('', 'test@example.com')",
    "SELECT * FROM users WHERE email = ''"
]

# Performance Tests
PERFORMANCE_TESTS = [
    "SELECT * FROM users LIMIT 1000",
    "SELECT * FROM products LIMIT 1000",
    "SELECT * FROM orders LIMIT 1000",
    "SELECT * FROM users JOIN orders ON users.id = orders.user_id JOIN products ON orders.product_id = products.id LIMIT 1000",
    "SELECT * FROM users WHERE id IN (1,2,3,4,5,6,7,8,9,10)",
    "SELECT * FROM users WHERE id BETWEEN 1 AND 100"
]

# Query Translation Tests
QUERY_TRANSLATION_TESTS = [
    "SELECT * FROM users",
    "SELECT name, email FROM users WHERE id = 1",
    "INSERT INTO users (name, email) VALUES ('John', 'john@example.com')",
    "UPDATE users SET email = 'updated@example.com' WHERE id = 1",
    "DELETE FROM users WHERE id = 1",
    "SELECT * FROM users ORDER BY id DESC",
    "SELECT * FROM users LIMIT 10",
    "SELECT * FROM users WHERE name = 'John'",
    "SELECT * FROM users WHERE id BETWEEN 1 AND 10",
    "SELECT * FROM users WHERE email LIKE '%example.com'"
]

# Connection Tests
CONNECTION_TESTS = [
    "SELECT 1",
    "SELECT version()",
    "SELECT current_database()",
    "SELECT current_user()",
    "SELECT now()",
    "SELECT pg_backend_pid()",
    "SELECT current_setting('timezone')",
    "SELECT current_setting('datestyle')",
    "SELECT current_setting('client_encoding')",
    "SELECT current_setting('lc_messages')"
]

# Schema Tests
SCHEMA_TESTS = [
    "SELECT * FROM information_schema.tables WHERE table_schema = 'public'",
    "SELECT * FROM information_schema.columns WHERE table_schema = 'public'",
    "SELECT table_name, column_name, data_type FROM information_schema.columns WHERE table_schema = 'public' ORDER BY table_name, ordinal_position",
    "SELECT * FROM pg_tables WHERE schemaname = 'public'",
    "SELECT * FROM pg_indexes WHERE schemaname = 'public'",
    "SELECT * FROM pg_constraints WHERE schema_name = 'public'",
    "SELECT * FROM pg_type WHERE typname LIKE '%text%'",
    "SELECT * FROM pg_type WHERE typname LIKE '%integer%'",
    "SELECT * FROM pg_type WHERE typname LIKE '%timestamp%'"
]

# Data Mapping Tests
DATA_MAPPING_TESTS = [
    "SELECT * FROM users WHERE name = 'John Doe'",
    "SELECT * FROM products WHERE price = 999.99",
    "SELECT * FROM orders WHERE quantity = 1",
    "SELECT * FROM users WHERE email = 'john@example.com'",
    "SELECT * FROM products WHERE category = 'Electronics'",
    "SELECT * FROM users WHERE created_at IS NOT NULL",
    "SELECT * FROM products WHERE created_at IS NOT NULL",
    "SELECT * FROM orders WHERE order_date IS NOT NULL",
    "SELECT * FROM users WHERE email LIKE '%example.com'",
    "SELECT * FROM products WHERE name LIKE '%Laptop%'"
]

# All Test Cases Combined
ALL_TEST_CASES = {
    "critical": CRITICAL_COMMANDS,
    "less_critical": LESS_CRITICAL_COMMANDS,
    "edge_cases": EDGE_CASES,
    "data_types": DATA_TYPE_TESTS,
    "error_handling": ERROR_HANDLING_TESTS,
    "performance": PERFORMANCE_TESTS,
    "query_translation": QUERY_TRANSLATION_TESTS,
    "connection": CONNECTION_TESTS,
    "schema": SCHEMA_TESTS,
    "data_mapping": DATA_MAPPING_TESTS
}

def get_test_case_summary():
    """Get a summary of all test cases."""
    summary = {
        "total_cases": 0,
        "critical": len(CRITICAL_COMMANDS),
        "less_critical": len(LESS_CRITICAL_COMMANDS),
        "edge_cases": len(EDGE_CASES),
        "data_types": len(DATA_TYPE_TESTS),
        "error_handling": len(ERROR_HANDLING_TESTS),
        "performance": len(PERFORMANCE_TESTS),
        "query_translation": len(QUERY_TRANSLATION_TESTS),
        "connection": len(CONNECTION_TESTS),
        "schema": len(SCHEMA_TESTS),
        "data_mapping": len(DATA_MAPPING_TESTS)
    }
    
    for key, value in summary.items():
        if key != "total_cases":
            summary["total_cases"] += value
    
    return summary

if __name__ == "__main__":
    summary = get_test_case_summary()
    print("Test Cases Summary:")
    print(f"Total Cases: {summary['total_cases']}")
    print(f"Critical: {summary['critical']}")
    print(f"Less Critical: {summary['less_critical']}")
    print(f"Edge Cases: {summary['edge_cases']}")
    print(f"Data Type Tests: {summary['data_types']}")
    print(f"Error Handling Tests: {summary['error_handling']}")
    print(f"Performance Tests: {summary['performance']}")
    print(f"Query Translation Tests: {summary['query_translation']}")
    print(f"Connection Tests: {summary['connection']}")
    print(f"Schema Tests: {summary['schema']}")
    print(f"Data Mapping Tests: {summary['data_mapping']}")
