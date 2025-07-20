"""API resources for F1 Monaco 2018 report generation.
This module defines the API endpoints for generating reports about the F1 Monaco in 2018,
including a general report and a detailed report of all drivers in RESTful format."""

from flask import Blueprint, request, abort, Response
from flask_restful import Api

from api.v1.utils import format_response
from db.models import Report, Driver
from db.middleware import BaseResource

api_bp = Blueprint("api_v1", __name__)
api = Api(api_bp)


class ReportResource(BaseResource):
    """Resource for generating F1 Monaco 2018 report."""

    def get(self) -> Response:
        """Generates a report of the F1 Monaco race report.
        :return: Response object with the report in the requested format."""

        order = request.args.get("order")
        if order and order not in {"asc", "desc"}:
            abort(400, description="Invalid order parameter")
        fmt = request.args.get("format", "json")
        query = (
            Report.select()
            .join(Driver)
            .order_by(Report.time.asc() if order else Report.time.desc())
        )
        result = [
            {
                "abbr": report.driver.abbr,
                "name": report.driver.name,
                "team": report.driver.team,
                "time": report.formatted_time,
            }
            for report in query
        ]
        return format_response(result, fmt)


class DriversResource(BaseResource):
    """Resource for generating report of all drivers and viewing individual driver information."""

    def get(self) -> Response:
        """Generates a report of all drivers or retrieves information for a specific driver.
        :return: Response object with the drivers report or individual driver information in the requested format.
        """

        fmt = request.args.get("format", "json")
        driver_id = request.args.get("driver_id")
        order_param = request.args.get("order")
        if order_param and order_param not in {"asc", "desc"}:
            abort(400, description="Invalid order parameter")
        order = order_param == "desc" if order_param in {"asc", "desc"} else False

        query = (
            Report.select(Report, Driver)
            .join(Driver)
            .order_by(Driver.name.asc() if not order else Driver.name.desc())
        )

        if driver_id:
            report = query.where(Driver.abbr == driver_id).first()
            if report:
                driver = [
                    {
                        "abbr": report.driver.abbr,
                        "name": report.driver.name,
                        "team": report.driver.team,
                        "time": report.formatted_time,
                    }
                ]
                return format_response(driver, fmt)
            abort(404, description="Driver not found")

        result = [
            {
                "abbr": r.driver.abbr,
                "name": r.driver.name,
                "team": r.driver.team,
            }
            for r in query
        ]
        return format_response(result, fmt)


api.add_resource(ReportResource, "/report/")
api.add_resource(DriversResource, "/report/drivers/")
