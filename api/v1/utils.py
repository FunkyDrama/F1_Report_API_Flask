"""Utility functions for serializing driver data and formatting responses.
This module provides functions to serialize driver information into a dictionary format
and format the response data into JSON or XML formats for Flask applications."""

from xml.etree import ElementTree as ET
from flask import jsonify, make_response, abort, Response


def serialize_driver(abbr: str, info: dict) -> dict:
    """Serialize driver information into a dictionary format.
    :param abbr: The driver's abbreviation.
    :param info: A dictionary containing driver's information.
    :return: A dictionary with driver's abbreviation, name, team, and time."""

    return {
        "abbr": abbr,
        "name": info["name"],
        "team": info["team"],
        "time": str(info["time"]).rstrip("0").rstrip(".") if info["time"] else "failed",
    }


def format_response(data: dict | list[dict], fmt: str) -> Response:
    """Format the response data into the requested format (JSON or XML).
    :param data: The data to format, can be a single dict or a list of dicts.
    :param fmt: The format to return the data in, either 'json' or 'xml'.
    :return: A Flask Response object with the formatted data.
    """

    if isinstance(data, dict):
        data = [data]

    if fmt.lower() == "json":
        return jsonify(data)

    elif fmt.lower() == "xml":
        root = ET.Element("drivers")
        for item in data:
            driver = ET.SubElement(root, "driver")
            for key, value in item.items():
                ET.SubElement(driver, key).text = str(value)
        xml_str = ET.tostring(root, encoding="utf-8")
        return make_response(xml_str, 200, {"Content-Type": "application/xml"})

    abort(400, description="Unsupported format. Use 'json' or 'xml'.")
