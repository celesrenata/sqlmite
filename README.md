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
pip install -r requirements.txt
```

## Usage

```python
import sqlite3
from sqlite_postgres_bridge import SQLitePostgreSQLBridge

# Connect to PostgreSQL through SQLite interface
conn = sqlite3.connect('database.db')
bridge = SQLitePostgreSQLBridge(conn, 'postgresql://user:pass@host:port/db')
```

## Architecture

The bridge implements a SQLite virtual table interface that translates SQLite operations to PostgreSQL queries.

## Testing

For end-to-end testing instructions, please refer to the [End-to-End Test Guide](docs/END_TO_END_TEST_GUIDE.md).
