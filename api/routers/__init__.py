"""
Routers package
"""
from .students import router as students_router
from .analytics import router as analytics_router

__all__ = [
    'students_router',
    'analytics_router'
]