# SQLite to PostgreSQL Bridge

This project provides a bridge that allows SQLite applications to access PostgreSQL databases transparently. It acts as a virtual SQLite database file that proxies all operations to a PostgreSQL backend.

## Features

- Transparent to SQLite applications
- Full PostgreSQL feature access
- Virtual filesystem node that mimics SQLite behavior
- Connection pooling and management
- Query translation between SQLite and PostgreSQL syntax

## MariaDB Support

The bridge now supports MariaDB as an alternative database provider, enabling transparent access to MariaDB databases through SQLite applications.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### PostgreSQL Usage

```python
import sqlite3
from sqlite_postgres_bridge import SQLitePostgreSQLBridge

# Connect to PostgreSQL through SQLite interface
conn = sqlite3.connect('database.db')
bridge = SQLitePostgreSQLBridge(conn, 'postgresql://user:pass@host:port/db')
```

### MariaDB Usage

```python
import sqlite3
from sqlite_postgres_bridge import MariaDBInterface

# Connect to MariaDB through SQLite interface
conn = sqlite3.connect('database.db')
mariadb_interface = MariaDBInterface(conn, 'mariadb://user:pass@host:port/db')
```

## Architecture

The bridge implements a SQLite virtual table interface that translates SQLite operations to PostgreSQL queries. The same interface can also work with MariaDB databases.

## Testing

For end-to-end testing instructions, please refer to the [End-to-End Test Guide](docs/END_TO_END_TEST_GUIDE.md).

## MariaDB Implementation

The MariaDB support is implemented in the `sqlite_postgres_bridge/mariadb_interface.py` module and provides:

- Full MariaDB connection management
- SQL query translation between SQLite and MariaDB
- Data type conversion between systems
- Transparent access to MariaDB databases through SQLite applications
- Proper error handling and resource management

## Requirements

- Python 3.6 or higher
- PostgreSQL client tools (psql) - for PostgreSQL support
- MariaDB client tools (mysql) - for MariaDB support
- Required Python packages (see requirements.txt)

## License

MIT License
