"""Test cases for the REST API endpoints of the racing report application.
This module contains tests for the API endpoints that generate reports about the F1 Monaco 2018.
"""

import pytest
from flask.testing import FlaskClient
from collections.abc import Iterator
from unittest.mock import patch

from api.rest_api import app

mock_report = [
    ("SVF", {"name": "Sebastian Vettel", "team": "FERRARI", "time": "0:01:04.415000"}),
    ("LHM", {"name": "Lewis Hamilton", "team": "MERCEDES", "time": "failed"}),
]


@pytest.fixture(autouse=True)
def mock_reportmaker() -> Iterator[None]:
    """Fixture for mocking ReportMaker.build_report."""
    with patch(
        "report.report_maker.ReportMaker.build_report",
        return_value=mock_report,
    ):
        yield


@pytest.fixture
def client() -> Iterator[FlaskClient]:
    """Fixture for creating a test Flask client."""
    with app.test_client() as client:
        yield client


def test_report_json(client: FlaskClient) -> None:
    """Test for getting the report in JSON format"""
    response = client.get("/api/v1/report/?format=json")
    assert response.status_code == 200
    assert response.is_json
    assert isinstance(response.get_json(), list)
    assert "abbr" in response.get_json()[0]


def test_report_xml(client: FlaskClient) -> None:
    """Test for getting the report in XML format"""
    response = client.get("/api/v1/report/?format=xml")
    assert response.status_code == 200
    assert response.content_type == "application/xml"
    assert b"<drivers>" in response.data


def test_report_order_asc(client: FlaskClient) -> None:
    """Test for sorting drivers by name in ascending order"""
    response = client.get("/api/v1/report/drivers/?order=asc&format=json")
    data = response.get_json()
    names = [d["name"] for d in data]
    assert names == sorted(names)


def test_report_order_desc(client: FlaskClient) -> None:
    """Test for sorting drivers by name in descending order"""
    response = client.get("/api/v1/report/drivers/?order=desc&format=json")
    data = response.get_json()
    names = [d["name"] for d in data]
    assert names == sorted(names, reverse=True)


def test_single_driver_json(client: FlaskClient) -> None:
    """Test for getting a single driver in JSON format"""
    response = client.get("/api/v1/report/drivers/?driver_id=SVF&format=json")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["abbr"] == "SVF"


def test_single_driver_xml(client: FlaskClient) -> None:
    """Test for getting a single driver in XML format"""
    response = client.get("/api/v1/report/drivers/?driver_id=SVF&format=xml")
    assert response.status_code == 200
    assert b"<driver>" in response.data
    assert b"SVF" in response.data


def test_driver_not_found(client: FlaskClient) -> None:
    """Test for handling a request for a non-existent driver"""
    response = client.get("/api/v1/report/drivers/?driver_id=ZZZ")
    assert response.status_code == 404
    assert b"Driver not found" in response.data


def test_invalid_format(client: FlaskClient) -> None:
    """Test for handling an unsupported format request"""
    response = client.get("/api/v1/report/?format=csv")
    assert response.status_code == 400
    assert b"Unsupported format" in response.data


def test_invalid_order_param(client: FlaskClient) -> None:
    """Test for handling an invalid order parameter"""
    response = client.get("/api/v1/report/drivers/?order=invalid")
    assert response.status_code == 400
    assert b"Invalid order parameter" in response.data
