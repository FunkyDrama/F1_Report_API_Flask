"""Тестування API додатку Flask для генерації звіту про гонку F1.
Цей модуль містить тести для перевірки коректності роботи API, включаючи генерацію звітів,
перегляд інформації про гонщиків та обробку помилок."""

import pytest
from collections.abc import Iterator
from flask.testing import FlaskClient
from unittest.mock import patch
from api.app import app
from bs4 import BeautifulSoup as bs


mock_report = [
    ("SVF", {"name": "Sebastian Vettel", "team": "FERRARI", "time": "0:01:04.415000"}),
    ("LHM", {"name": "Lewis Hamilton", "team": "MERCEDES", "time": "failed"}),
]


@pytest.fixture
def client() -> Iterator[FlaskClient]:
    """Фікстура для створення тестового клієнта Flask."""
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def mock_reportmaker() -> Iterator[None]:
    """Фікстура для мокування ReportMaker.build_report."""
    with patch(
        "report.report_maker.ReportMaker.build_report", return_value=mock_report
    ):
        yield


def test_report(client: FlaskClient) -> None:
    """Тест для перевірки генерації звіту про гонку."""
    response = client.get("/report/")
    assert response.status_code == 200
    assert b"F1 Monaco 2018 Report" in response.data


def test_report_sorted(client: FlaskClient) -> None:
    """Тест для перевірки сортування гонщиків у звіті."""
    response = client.get("/report/?order=asc")
    soup = bs(response.data, "html.parser")
    drivers = [td.text for td in soup.find_all("td")[4::5]]
    assert drivers == sorted(drivers)

    response_desc = client.get("/report/?order=desc")
    soup_desc = bs(response_desc.data, "html.parser")
    drivers_desc = [td.text for td in soup_desc.find_all("td")[4::5]]
    assert drivers_desc == sorted(drivers_desc, reverse=True)


def test_report_drivers(client: FlaskClient) -> None:
    """Тест для перевірки генерації звіту про гонщиків."""
    response = client.get("/report/drivers/")
    assert response.status_code == 200
    assert b"Drivers list" in response.data


def test_report_drivers_sorted_names(client: FlaskClient) -> None:
    """Тест для перевірки сортування гонщиків за іменами у звіті про гонщиків."""
    response = client.get("/report/drivers/?order=asc")
    soup = bs(response.data, "html.parser")
    names = [td.text for td in soup.find_all("td")[2::4]]
    assert names == sorted(names)

    response_desc = client.get("/report/drivers/?order=desc")
    soup_desc = bs(response_desc.data, "html.parser")
    names_desc = [td.text for td in soup_desc.find_all("td")[2::4]]
    assert names_desc == sorted(names_desc, reverse=True)


def test_report_driver_info(client: FlaskClient) -> None:
    """Тест для перевірки перегляду інформації про окремого гонщика."""
    response = client.get("/report/drivers/?driver_id=SVF")
    assert response.status_code == 200
    assert b"Sebastian Vettel" in response.data
    assert b"FERRARI" in response.data


def test_report_driver_not_found(client: FlaskClient) -> None:
    """Тест для перевірки обробки помилки при відсутності гонщика."""
    response = client.get("/report/drivers/?driver_id=XYZ")
    assert response.status_code == 404
    assert b"Driver not found" in response.data


def test_report_invalid_order(client: FlaskClient) -> None:
    """Тест для перевірки обробки помилки при некоректному параметрі order."""
    response = client.get("/report/drivers/?order=invalid")
    assert response.status_code == 400
    assert b"Invalid order parameter" in response.data
