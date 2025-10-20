"""
SQLite to PostgreSQL Bridge
A bridge that allows SQLite applications to access PostgreSQL databases transparently.
"""

__version__ = "0.1.0"
__author__ = "SQLite PostgreSQL Bridge Team"

# Import core components
from .bridge import SQLitePostgreSQLBridge
from .virtual_table_interface import VirtualTableInterface

# Import supporting components
from .connection_manager import ConnectionManager
from .query_translator import QueryTranslator
from .data_mapper import DataMapper

# Import MariaDB support
from .mariadb_interface import MariaDBInterface

# Import CLI
from .cli import main

__all__ = [
    "SQLitePostgreSQLBridge",
    "VirtualTableInterface",
    "ConnectionManager", 
    "QueryTranslator",
    "DataMapper",
    "MariaDBInterface",
    "main"
]
