"""Middleware for managing database sessions in Flask-RESTful resources.
This module provides a session management decorator for Flask-RESTful resources,
ensuring that database sessions are properly opened and closed around resource methods.
"""

from collections.abc import Callable
from functools import wraps
from flask_restful import Resource

from db.config import db


def session(func: Callable) -> Callable:
    """Middleware to manage database sessions for functions that require a session."""

    @wraps(func)
    def wrapper(*args, **kwargs) -> Callable:
        """Wrapper function to ensure the database session is open before executing the function."""
        if db.is_closed():
            db.connect()
        try:
            return func(*args, **kwargs)
        finally:
            if not db.is_closed():
                db.close()

    return wrapper


class BaseResource(Resource):
    """Base resource class for Flask-RESTful resources with session management."""

    method_decorators = [session]
