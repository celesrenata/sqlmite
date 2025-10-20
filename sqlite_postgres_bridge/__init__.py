"""
SQLite to PostgreSQL Bridge
A bridge that allows SQLite applications to access PostgreSQL databases transparently.
"""

__version__ = "0.1.0"
__author__ = "SQLite PostgreSQL Bridge Team"

from .bridge import SQLitePostgreSQLBridge

__all__ = ["SQLitePostgreSQLBridge"]
