"""API resources for F1 Monaco 2018 report generation.
This module defines the API endpoints for generating reports about the F1 Monaco in 2018,
including a general report and a detailed report of all drivers in RESTful format."""

from flask import Blueprint, request, abort, Response
from flask_restful import Api, Resource

from api.v1.utils import serialize_driver, format_response
from report.report_maker import ReportMaker

api_bp = Blueprint("api_v1", __name__)
api = Api(api_bp)


class ReportResource(Resource):
    """Resource for generating F1 Monaco 2018 report."""

    def get(self) -> Response:
        """Generates a report of the F1 Monaco race report.
        :return: Response object with the report in the requested format."""

        order = request.args.get("order") == "desc"
        fmt = request.args.get("format", "json")

        report = ReportMaker().build_report(asc=not order)
        result = [serialize_driver(abbr, info) for abbr, info in report]
        return format_response(result, fmt)


class DriversResource(Resource):
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

        report = ReportMaker().build_report()

        if driver_id:
            for abbr, info in report:
                if abbr == driver_id:
                    return format_response(serialize_driver(abbr, info), fmt)
            abort(404, description="Driver not found")

        sorted_report = sorted(report, key=lambda item: item[1]["name"], reverse=order)
        result = [serialize_driver(abbr, info) for abbr, info in sorted_report]
        return format_response(result, fmt)


api.add_resource(ReportResource, "/report/")
api.add_resource(DriversResource, "/report/drivers/")
