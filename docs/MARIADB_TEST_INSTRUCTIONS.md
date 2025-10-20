# MariaDB Test Instructions for Amazon Q

This document provides detailed instructions for testing the MariaDB support in the SQLite to PostgreSQL bridge. These instructions are designed to be ingested by Amazon Q for automated testing and validation.

## Prerequisites

Before running the MariaDB tests, ensure the following are installed:

1. **Python 3.6 or higher**
2. **MariaDB client tools** (if needed for manual testing)
3. **Required Python packages**:
   ```bash
   pip install -r requirements.txt
   ```

## Test Environment Setup

### 1. Database Configuration

The MariaDB tests require access to the test database with the following credentials:
- **Host**: 10.1.1.12 (same as PostgreSQL)
- **Port**: 3306 (MariaDB default)
- **Database**: sqlmite
- **Username**: sqlmite
- **Password**: PSCh4ng3me!

### 2. Test Data Preparation

The MariaDB tests will automatically prepare the database with test data. However, you can manually prepare it by running:

```bash
# Connect to MariaDB (if needed for manual preparation)
mysql -h 10.1.1.12 -P 3306 -u sqlmite -p
```

Then create the test schema:
```sql
-- Create test tables if needed
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2),
    category VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT REFERENCES users(id),
    product_id INT REFERENCES products(id),
    quantity INT NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert some test data
INSERT INTO users (name, email) VALUES 
    ('John Doe', 'john@example.com'),
    ('Jane Smith', 'jane@example.com'),
    ('Bob Johnson', 'bob@example.com');

INSERT INTO products (name, price, category) VALUES 
    ('Laptop', 999.99, 'Electronics'),
    ('Book', 19.99, 'Education'),
    ('Coffee Mug', 12.50, 'Kitchen');
```

## MariaDB Test Suite Components

### 1. MariaDB Interface Tests

**Location**: `tests/test_mariadb_interface.py`

**Purpose**: Tests all MariaDB interface components.

**Usage**:
```bash
# Run MariaDB interface tests
python -m pytest tests/test_mariadb_interface.py -v
```

**Test Categories**:
- **Connection Manager Tests**: Tests MariaDB connection handling
- **Query Translator Tests**: Tests SQL translation functionality
- **Data Mapper Tests**: Tests data type conversions
- **Interface Tests**: Tests complete MariaDB interface functionality

### 2. Full MariaDB Integration Tests

**Location**: `scripts/full_functionality_test.py`

**Purpose**: Comprehensive test of all MariaDB functionality.

**Usage**:
```bash
# Run full MariaDB functionality test
python scripts/full_functionality_test.py
```

## Test Cases Organization

### Critical MariaDB Tests
These tests must pass for the MariaDB support to be functional:
- MariaDB connection initialization
- Basic query execution
- DML operations (INSERT, UPDATE, DELETE)
- Data type conversions
- Resource cleanup

### Less Critical MariaDB Tests
These should work but are not critical:
- Complex query translations
- Advanced data mapping
- Performance considerations

### Edge Cases
Special handling scenarios:
- NULL value handling
- Special character handling
- Error condition testing
- Connection timeout handling

## Running Tests

### 1. Unit Tests
```bash
# Run all MariaDB unit tests
python -m pytest tests/test_mariadb_interface.py -v
```

### 2. Integration Tests
```bash
# Run full functionality test
python scripts/full_functionality_test.py
```

### 3. Specific Component Tests
```bash
# Test connection manager
python -m pytest tests/test_mariadb_interface.py::TestMariaDBConnectionManager -v

# Test query translator
python -m pytest tests/test_mariadb_interface.py::TestMariaDBQueryTranslator -v

# Test data mapper
python -m pytest tests/test_mariadb_interface.py::TestMariaDBDataMapper -v

# Test interface
python -m pytest tests/test_mariadb_interface.py::TestMariaDBInterface -v
```

## Expected Results

### Successful Execution
- All MariaDB tests should pass
- Connection manager should initialize correctly
- Query translator should handle basic operations
- Data mapper should handle type conversions
- Interface should work with MariaDB backend

### Error Conditions
The test suite should:
- Report specific errors for failed tests
- Continue with other tests when one fails
- Provide clear error messages for debugging

## Troubleshooting

### Connection Issues
If you encounter connection problems:
1. Verify network connectivity to 10.1.1.12
2. Check MariaDB server is running on port 3306
3. Verify credentials are correct
4. Ensure firewall allows connections on port 3306

### Permission Issues
If you get permission errors:
1. Verify user 'sqlmite' has access to database 'sqlmite'
2. Check MariaDB user permissions
3. Ensure the user can connect to the database

### Python Environment Issues
If you encounter Python errors:
1. Verify all dependencies are installed: `pip install -r requirements.txt`
2. Check Python version compatibility
3. Ensure the package is installed in development mode

## Integration with Amazon Q

The MariaDB test suite is designed to be easily ingested by Amazon Q:
- All test scripts are self-contained
- Clear parameter specifications
- Comprehensive documentation
- Standard Python execution patterns
- Automated testing capabilities

## Test Coverage

The MariaDB test suite provides comprehensive coverage of:
- Database connection and authentication
- Basic CRUD operations
- Advanced query operations
- Data type conversions
- Error handling
- Performance considerations
- Edge case scenarios

## MariaDB-Specific Testing

### Connection Testing
```bash
# Test MariaDB connection
python -c "
from sqlite_postgres_bridge.mariadb_interface import MariaDBConnectionManager
manager = MariaDBConnectionManager('mariadb://sqlmite:PSCh4ng3me!@10.1.1.12:3306/sqlmite')
print('MariaDB connection test:', manager.test_connection())
"
```

### Query Translation Testing
```bash
# Test query translation
python -c "
from sqlite_postgres_bridge.mariadb_interface import MariaDBQueryTranslator
translator = MariaDBQueryTranslator()
query = 'SELECT * FROM users WHERE id = 1'
translated = translator.translate(query)
print('Query translation test:', translated)
"
```

## MariaDB Integration Testing

The MariaDB support can now be tested with:

1. **Unit Testing**:
   ```bash
   python -m pytest tests/test_mariadb_interface.py -v
   ```

2. **Full Functionality Testing**:
   ```bash
   python scripts/full_functionality_test.py
   ```

3. **Manual Testing**:
   ```bash
   # Test CLI connection
   sqlite-postgres-bridge --help
   ```

The MariaDB support is now fully integrated and ready for Amazon Q integration, providing transparent access to MariaDB databases through the SQLite to PostgreSQL bridge.
