# Test Suite Instructions for Amazon Q Integration

This document provides detailed instructions for running the SQLite to PostgreSQL bridge test suite. These instructions are designed to be ingested by Amazon Q for automated testing and validation.

## Prerequisites

Before running the test suite, ensure the following are installed:

1. **Python 3.6 or higher**
2. **PostgreSQL client tools (psql)**
3. **Required Python packages**:
   ```bash
   pip install -r requirements.txt
   ```

## Test Environment Setup

### 1. Database Configuration

The test suite requires access to the test database with the following credentials:
- **Host**: your.database.host (or backup.host1, backup.host2)
- **Port**: 5432
- **Database**: testdb
- **Username**: your_username
- **Password**: your_password

### 2. Test Data Preparation

The test suite automatically prepares the database with test data. However, you can manually prepare it by running:

```bash
psql -h your.database.host -p 5432 -U your_username -d testdb
```

Then create the test schema:
```sql
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2),
    category VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (name, email) VALUES 
    ('John Doe', 'john@example.com'),
    ('Jane Smith', 'jane@example.com'),
    ('Bob Johnson', 'bob@example.com');

INSERT INTO products (name, price, category) VALUES 
    ('Laptop', 999.99, 'Electronics'),
    ('Book', 19.99, 'Education'),
    ('Coffee Mug', 12.50, 'Kitchen');
```

## Test Suite Components

### 1. Database Reset Script

**Location**: `scripts/reset_test_database.py`

**Purpose**: Resets the test database to a known initial state.

**Usage**:
```bash
python scripts/reset_test_database.py
```

**Parameters**: 
- Host: your.database.host (default)
- Port: 5432 (default)
- Database: testdb (default)
- Username: celes (default)
- Password: PSCh4ng3me! (default)

### 2. Test Suite Runner

**Location**: `scripts/test_suite_runner.py`

**Purpose**: Orchestrates the complete test execution.

**Usage**:
```bash
python scripts/test_suite_runner.py
```

**Execution Flow**:
1. Reset database to initial state
2. Run unit tests
3. Run integration tests
4. Run end-to-end tests

### 3. Active Test Suite

**Location**: `scripts/active_test_suite.py`

**Purpose**: Runs comprehensive active tests against the database.

**Usage**:
```bash
python scripts/active_test_suite.py
```

**Test Categories**:
- **Critical Tests**: Basic database operations (SELECT, INSERT, UPDATE, DELETE)
- **Less Critical Tests**: Advanced operations (JOINs, GROUP BYs)
- **Edge Case Tests**: Special handling (NULL values, LIKE patterns)

## Makefile Integration

The project includes a Makefile for easier test execution:

```bash
make test-suite      # Run complete test suite
make test-active   # Run active tests only
make test-unit     # Run unit tests only
make reset-db        # Reset test database
make cli-test        # Test CLI functionality
make build          # Build the package
make install        # Install the package
```

## CLI Integration Testing

The bridge includes a command-line interface that can be used to test connectivity:

```bash
# Test basic CLI help
sqlite-postgres-bridge --help

# Test CLI with parameters (creates a functional bridge connection)
sqlite-postgres-bridge --sqlite-db test.db --postgres-url "postgresql://your_username:your_password@your.database.host:5432/testdb"
```

## Test Cases Organization

### Critical Commands
These commands must work for the bridge to be functional:
- Basic SELECT operations
- Basic INSERT operations  
- Basic UPDATE operations
- Basic DELETE operations
- COUNT operations

### Less Critical Commands
These should work but are not critical:
- JOIN queries
- GROUP BY operations
- Complex WHERE clauses
- Advanced filtering

### Edge Cases
Special handling scenarios:
- NULL value handling
- Special character handling
- Error condition testing
- Data type conversions

## Running Tests

### 1. Full Test Suite
```bash
python scripts/test_suite_runner.py
```

### 2. Individual Test Components
```bash
# Run database reset
python scripts/reset_test_database.py

# Run active tests
python scripts/active_test_suite.py
```

### 3. Unit Tests
```bash
pytest -v
```

## Expected Results

### Successful Execution
- All critical tests should pass
- Less critical tests should pass
- Edge case tests should handle gracefully
- Database should be reset properly between runs

### Error Conditions
The test suite should:
- Report specific errors for failed tests
- Continue with other tests when one fails
- Provide clear error messages for debugging

## Troubleshooting

### Connection Issues
If you encounter connection problems:
1. Verify network connectivity to 10.1.1.12
2. Check PostgreSQL server is running
3. Verify credentials are correct
4. Ensure firewall allows connections on port 5432

### Permission Issues
If you get permission errors:
1. Verify user 'celes' has access to database 'testdb'
2. Check PostgreSQL role permissions
3. Ensure the user can connect to the database

### Python Environment Issues
If you encounter Python errors:
1. Verify all dependencies are installed: `pip install -r requirements.txt`
2. Check Python version compatibility
3. Ensure the package is installed in development mode

### NixOS Specific Instructions
If you're using NixOS, you may need to run:
```bash
nix-shell -p postgresql
```

### Database Setup Issues
If you encounter database setup issues:
1. Make sure PostgreSQL is installed and running
2. Create the test database: `createdb testdb`
3. Ensure the user 'celes' exists with proper permissions
4. Run the reset script: `python scripts/reset_test_database.py`

## Integration with Amazon Q

The test suite is designed to be easily ingested by Amazon Q:
- All test scripts are self-contained
- Clear parameter specifications
- Comprehensive documentation
- Standard Python execution patterns
- Automated reset functionality

## Test Coverage

The test suite provides comprehensive coverage of:
- Database connection and authentication
- Basic CRUD operations
- Advanced query operations
- Data type conversions
- Error handling
- Performance considerations
- Edge case scenarios

## Bridge Integration Testing

The bridge can now be tested with:

1. **CLI Testing**:
   ```bash
   sqlite-postgres-bridge --sqlite-db test.db --postgres-url "postgresql://your_username:your_password@your.database.host:5432/testdb"
   ```

2. **Database Testing**:
   ```bash
   make test-suite
   ```

3. **Active Testing**:
   ```bash
   make test-active
   ```

4. **Unit Testing**:
   ```bash
   make test-unit
   ```

5. **CLI Connection Testing**:
   ```bash
   # Test CLI connection establishment
   sqlite-postgres-bridge --sqlite-db test.db --postgres-url "postgresql://your_username:your_password@your.database.host:5432/testdb"
   ```

The bridge now provides a functional connection between SQLite and PostgreSQL databases, enabling comprehensive testing of database operations. The CLI now properly tests connections when parameters are provided.
