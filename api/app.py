"""Генератор звіту про гонку F1 Monaco 2018.
Цей модуль містить Flask-додаток, який надає API для генерації звітів про гонку та гонщиків.
"""

from flask import Flask, render_template, request, abort, Response
from report.report_maker import ReportMaker
from pathlib import Path

BASE_DIR = Path(__file__).parent
TEMPLATE_DIR = BASE_DIR / "templates"
app = Flask(__name__, template_folder=str(TEMPLATE_DIR))


@app.route("/report/")
def report() -> str:
    """Генератор звіту про гонку F1 Monaco 2018.
    :return: HTML-сторінка зі звітом про гонку."""

    order = request.args.get("order", True)
    order = True if order == "desc" else False
    all_report = ReportMaker().build_report(asc=order)
    return render_template("index.html", report=all_report)


@app.route("/report/drivers/")
def report_drivers() -> str | Response:
    """Генератор звіту про всіх гонщиків та перегляд інформації про окремого гонщика.
    :return: HTML-сторінка зі звітом про гонщиків або інформацією про окремого гонщика.
    """

    order_param = request.args.get("order")
    if order_param and order_param not in {"asc", "desc"}:
        abort(400, description="Invalid order parameter")
    order = order_param == "desc"

    all_drivers_report = ReportMaker().build_report()

    driver_id = request.args.get("driver_id")
    if driver_id:
        for abbr, info in all_drivers_report:
            if abbr == driver_id:
                return render_template("driver.html", abbr=abbr, info=info)
        abort(404, description="Driver not found")
    else:
        sorted_drivers = sorted(
            all_drivers_report,
            key=lambda item: item[1]["name"],
            reverse=order,
        )
    return render_template("drivers.html", drivers=sorted_drivers, driver_id=driver_id)
