# SQLite to PostgreSQL Bridge

This project provides a bridge that allows SQLite applications to access PostgreSQL databases transparently. It acts as a virtual SQLite database file that proxies all operations to a PostgreSQL backend.

## Features

- Transparent to SQLite applications
- Full PostgreSQL feature access
- Virtual filesystem node that mimics SQLite behavior
- Connection pooling and management
- Query translation between SQLite and PostgreSQL syntax

## Installation

```bash
# Clone the repository
git clone https://github.com/celesrenata/sqlmite.git
cd sqlmite

# Install in development mode
pip install -e .
```

## Quick Start

```python
import sqlite3
from sqlite_postgres_bridge import SQLitePostgreSQLBridge

# Connect to PostgreSQL through SQLite interface
conn = sqlite3.connect(':memory:')
postgres_url = "postgresql://user:pass@host:port/database"
bridge = SQLitePostgreSQLBridge(conn, postgres_url)
```

## Command Line Interface

```bash
# Show help
sqlite-postgres-bridge --help

# Show version
sqlite-postgres-bridge --version

# Connect databases (future feature)
sqlite-postgres-bridge --sqlite-db app.db --postgres-url "postgresql://user:pass@host:port/db"
```

## Testing

### Quick Test (No Database Required)
```bash
# Run end-to-end functionality test
python test_bridge_e2e.py
```

### Unit Tests
```bash
# Run all tests
python -m pytest tests/ -v

# Run core functionality tests only
python -m pytest tests/test_query_translator.py tests/test_data_mapper.py -v
```

### Full Integration Test
Requires PostgreSQL server. See [End-to-End Test Guide](docs/END_TO_END_TEST_GUIDE.md) for details.

## Architecture

The bridge implements a SQLite virtual table interface that translates SQLite operations to PostgreSQL queries.

### Components

- **Bridge**: Main interface coordinating all components
- **Query Translator**: Converts SQLite SQL to PostgreSQL SQL
- **Data Mapper**: Maps PostgreSQL results to SQLite format
- **Connection Manager**: Handles PostgreSQL connection pooling

## Development Status

✅ **Working Components:**
- CLI interface
- Query translation
- Data mapping
- Connection management
- Bridge initialization

⚠️ **Requires PostgreSQL for full testing:**
- Virtual table implementation
- Real-time query execution
- Transaction management

## Contributing

1. Fork the repository
2. Create a feature branch
3. Run tests: `python test_bridge_e2e.py`
4. Submit a pull request

## License

MIT License - see LICENSE file for details.
