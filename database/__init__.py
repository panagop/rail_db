"""
Database package for rail_db project.

This package contains all database-related functionality including:
- Connection management
- Data import utilities
- Analytics and reporting
- Test functions
"""

from .connection import DatabaseConnection, DatabaseManager
from .analytics import StudentAnalytics

__all__ = [
    'DatabaseConnection',
    'DatabaseManager', 
    'StudentAnalytics'
]