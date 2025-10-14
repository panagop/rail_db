"""
API package for the rail_db FastAPI service.

This package contains:
- FastAPI routers for different endpoints
- Pydantic models for request/response validation
- Dependencies and middleware
"""

from .dependencies import get_database_manager
from .main import app

__all__ = [
    'app',
    'get_database_manager'
]