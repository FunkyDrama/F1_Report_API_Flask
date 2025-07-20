"""Database models for the application using Peewee ORM.
This module defines the Driver and Report models with their fields and relationships."""

from peewee import *
from db.config import BaseModel


class Driver(BaseModel):
    """Model representing a driver in the application."""

    abbr = CharField(unique=True, max_length=3)
    name = CharField()
    team = CharField()

    class Meta:
        indexes = ((("abbr", "name"), True),)


class Report(BaseModel):
    """Model representing a report associated with a driver."""

    driver = ForeignKeyField(Driver, backref="reports")
    time = IntegerField(null=True)

    @property
    def formatted_time(self) -> str:
        """Format the time in minutes:seconds.milliseconds."""
        if self.time is None:
            return "failed"
        minutes = self.time // (60 * 1000)
        seconds = (self.time % (60 * 1000)) // 1000
        ms = self.time % 1000
        return f"{minutes}:{seconds:02d}.{ms:03d}"

    class Meta:
        indexes = ((("driver",), True),)
