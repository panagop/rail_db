"""
FastAPI dependencies
"""
from database import DatabaseManager


def get_database_manager():
    """Dependency to provide database manager"""
    return DatabaseManager()