# End-to-End Testing Guide

This guide provides step-by-step instructions for testing the SQLite to PostgreSQL bridge.

## Prerequisites

Before beginning, ensure you have:
1. Python 3.6 or higher installed
2. Optional: PostgreSQL server for full integration testing
3. Test database credentials (if using real PostgreSQL):
   - Host: 10.1.1.12 (or 10.1.13, 10.1.1.14)
   - Port: 5432
   - Database: testdb
   - Username: celes
   - Password: PSCh4ng3me!

## Quick Start

### 1. Install the Bridge Package

```bash
# Clone the project
git clone https://github.com/celesrenata/sqlmite.git
cd sqlmite

# Install in development mode
pip install -e .
```

### 2. Run End-to-End Tests

```bash
# Run the comprehensive test suite
python test_bridge_e2e.py
```

Expected output:
```
Starting end-to-end test for SQLite to PostgreSQL bridge
============================================================

✓ SQLite connection established
✓ Bridge initialization completed
✓ Basic operations test completed
✓ Cleanup completed

Testing query translation...
SQLite: SELECT * FROM users WHERE id = 1
PostgreSQL: SELECT * FROM users WHERE id = 1
✓ Query translation test completed

Testing data mapping...
Mapped results: [{'id': 1, 'name': 'John Doe', 'email': 'john@example.com'}, {'id': 2, 'name': 'Jane Smith', 'email': 'jane@example.com'}]
✓ Data mapping test completed

============================================================
✓ All tests passed!
```

### 3. Test CLI Functionality

```bash
# Test CLI help
sqlite-postgres-bridge --help

# Test version
sqlite-postgres-bridge --version
```

### 4. Run Unit Tests

```bash
# Run all unit tests
python -m pytest tests/ -v

# Run only tests that don't require database connection
python -m pytest tests/test_query_translator.py tests/test_data_mapper.py -v
```

## Full Integration Testing (Requires PostgreSQL)

If you have access to a PostgreSQL server, you can test full integration:

### 1. Create Test Database Schema

```bash
psql -h <host> -p 5432 -U <username> -d <database>
```

Create test table:
```sql
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (name, email) VALUES 
    ('John Doe', 'john@example.com'),
    ('Jane Smith', 'jane@example.com'),
    ('Bob Johnson', 'bob@example.com');
```

### 2. Test with Real Database

```python
import sqlite3
from sqlite_postgres_bridge import SQLitePostgreSQLBridge

# Connect with real PostgreSQL
sqlite_conn = sqlite3.connect(':memory:')
postgres_url = "postgresql://username:password@host:port/database"
bridge = SQLitePostgreSQLBridge(sqlite_conn, postgres_url)

# Test operations (implementation dependent)
```

## Test Results Analysis

### Expected Test Outcomes

**✅ Working Components:**
- CLI functionality (`--help`, `--version`)
- Bridge object creation and initialization
- Query translation (SQLite ↔ PostgreSQL)
- Data mapping (PostgreSQL results → SQLite format)
- Connection manager (when PostgreSQL available)

**⚠️ Database-Dependent Tests:**
- Some unit tests require actual PostgreSQL connection
- Bridge tests will fail without running PostgreSQL server
- This is expected behavior for offline testing

### Unit Test Results
```bash
# Typical results without PostgreSQL server:
# 16 passed, 7 failed (connection-dependent tests)
# All core functionality tests pass
```

## Troubleshooting

### Connection Issues
- **No PostgreSQL server**: Expected - core functionality still works
- **Network connectivity**: Verify host/port accessibility
- **Authentication**: Check username/password credentials

### Installation Issues
```bash
# Reinstall if needed
pip uninstall sqlite-postgres-bridge
pip install -e .
```

### Python Environment
```bash
# Verify installation
python -c "import sqlite_postgres_bridge; print('✓ Import successful')"
```

## Development Testing

For development and CI/CD environments without PostgreSQL:

```bash
# Test core functionality only
python test_bridge_e2e.py

# Test individual components
python -m pytest tests/test_query_translator.py tests/test_data_mapper.py -v
```

This ensures the bridge logic works correctly even without database connectivity.

## Next Steps

After successful testing:
1. Integrate bridge into your applications
2. Configure with your PostgreSQL credentials
3. Extend functionality as needed
4. Add application-specific tests
