"""Database configuration for the report application.
This module defines the database connection and base model for the application."""

from peewee import Model, SqliteDatabase

db = SqliteDatabase("report.db")


class BaseModel(Model):
    """Base model class for all database models."""

    class Meta:
        database = db
