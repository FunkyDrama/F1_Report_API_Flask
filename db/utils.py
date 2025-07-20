"""Utility functions for database operations.
This module provides functions to initialize the database and convert time formats."""

import datetime

from db.config import db
from db.models import Driver, Report
from report.report_maker import ReportMaker


def init_db() -> None:
    """Initialize the database and create tables if they do not exist."""
    db.create_tables([Driver, Report], safe=True)
    with db.atomic():
        report_maker = ReportMaker()
        drivers = report_maker.build_report()
        for abbr, info in drivers:
            driver, created = Driver.get_or_create(
                abbr=abbr,
                defaults={"name": info["name"], "team": info["team"]},
            )
            if not created:
                driver.name = info["name"]
                driver.team = info["team"]
                driver.save()

            Report.get_or_create(
                driver=driver,
                time=timedelta_to_milliseconds(
                    info["time"],
                ),
            )


def timedelta_to_milliseconds(td: datetime.timedelta) -> int | None:
    """Convert a timedelta object to milliseconds.
    :param td: A timedelta object.
    :return: The total number of milliseconds as an integer."""

    if not isinstance(td, datetime.timedelta):
        return None
    total_seconds = td.total_seconds()
    return int(total_seconds * 1000)
