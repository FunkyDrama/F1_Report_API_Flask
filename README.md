# F1 Monaco 2018 Race Report Generator

A Python application for parsing lap-time logs and generating reports of the F1 Monaco 2018 Grand Prix. Provides CLI, Web UI, and REST API interfaces.

## Table of Contents

* [Overview](#overview)
* [Features](#features)
* [Prerequisites](#prerequisites)
* [Installation](#installation)
* [Usage](#usage)
  * [CLI](#cli)
  * [Web UI](#web-ui)
  * [REST API](#rest-api)
* [API Documentation](#api-documentation)
* [Project Structure](#project-structure)
* [Testing](#testing)
* [License](#license)

## Overview

This Python application reads three files—`start.log`, `end.log`, and `abbreviations.txt`—to compute each driver's total lap time for the 2018 Monaco Grand Prix. The results can be accessed via:

- **CLI** — command-line interface for quick reports
- **Web UI** — browser-based interface with HTML templates
- **REST API** — RESTful endpoints with JSON/XML responses and Swagger documentation

## Features

* Parses timestamped log files and driver abbreviations
* Calculates total race time for each competitor
* Supports sorting results in ascending (fastest first) or descending (slowest first) order
* Optional filtering to display a specific driver's result
* SQLite database with Peewee ORM for data persistence
* RESTful API with JSON and XML response formats
* Interactive Swagger API documentation
* Web interface with Jinja2 templates

## Prerequisites

* Python 3.12 or higher
* Poetry (for dependency management)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/FunkyDrama/F1_Report_API_Flask.git
   cd F1_Report_API_Flask
   ```

2. Install dependencies using Poetry:

   ```bash
   poetry install
   ```

3. Ensure the input files are in the `data/` folder:
   * `start.log`
   * `end.log`
   * `abbreviations.txt`

## Usage

### CLI

Run the CLI tool using the installed script or directly via Python:

```bash
# Using installed script
report-of-monaco-2018-racing --files ./data

# Or directly
python -m report.main --files ./data
```

#### CLI Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--files` | Yes | Path to directory with log files |
| `--asc` | No | Sort ascending (fastest first, default) |
| `--desc` | No | Sort descending (slowest first) |
| `--driver NAME` | No | Show only specific driver's result |

#### CLI Examples

```bash
# Default ascending leaderboard
report-of-monaco-2018-racing --files ./data

# Descending leaderboard
report-of-monaco-2018-racing --files ./data --desc

# Specific driver
report-of-monaco-2018-racing --files ./data --driver "Lewis Hamilton"
```

### Web UI

Start the web application:

```bash
python -m api.app
```

Open in browser:
- **Race Report:** http://localhost:5000/report/
- **Drivers List:** http://localhost:5000/report/drivers/
- **Driver Details:** http://localhost:5000/report/drivers/?driver_id=VET

Query parameters:
- `order` — `asc` or `desc` for sorting
- `driver_id` — driver abbreviation (e.g., `VET`, `HAM`)

### REST API

Start the API server:

```bash
python -m api.rest_api
```

#### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/report/` | Full race report |
| GET | `/api/v1/report/drivers/` | All drivers or specific driver |

#### Query Parameters

| Parameter | Values | Description |
|-----------|--------|-------------|
| `format` | `json`, `xml` | Response format (default: json) |
| `order` | `asc`, `desc` | Sort order |
| `driver_id` | e.g., `VET` | Filter by driver (drivers endpoint) |

#### API Examples

```bash
# Get full report as JSON
curl http://localhost:5000/api/v1/report/

# Get report sorted ascending as XML
curl "http://localhost:5000/api/v1/report/?order=asc&format=xml"

# Get specific driver
curl "http://localhost:5000/api/v1/report/drivers/?driver_id=VET"

# Get all drivers sorted by name
curl "http://localhost:5000/api/v1/report/drivers/?order=asc"
```

## API Documentation

Swagger UI is available at http://localhost:5000/apidocs/ when the REST API server is running.

## Project Structure

```
report-of-monaco-2018-racing/
├── api/
│   ├── __init__.py
│   ├── app.py                    # Web UI Flask application
│   ├── rest_api.py               # REST API entry point
│   ├── templates/                # Jinja2 HTML templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── drivers.html
│   │   └── driver.html
│   └── v1/
│       ├── __init__.py
│       ├── resources.py          # API resource classes
│       ├── utils.py              # Response formatting utilities
│       └── docs/
│           └── swagger_spec.yml  # Swagger/OpenAPI specification
├── db/
│   ├── __init__.py
│   ├── config.py                 # Database configuration
│   ├── middleware.py             # Database middleware
│   ├── models.py                 # Peewee ORM models (Driver, Report)
│   └── utils.py                  # Database utilities
├── report/
│   ├── __init__.py
│   ├── main.py                   # CLI entry point
│   └── report_maker.py           # Report generation logic
├── tests/
│   ├── __init__.py
│   ├── test_app.py               # Web UI tests
│   └── test_rest_api.py          # REST API tests
├── data/                         # Input data files
│   ├── start.log
│   ├── end.log
│   └── abbreviations.txt
├── pyproject.toml                # Project configuration and dependencies
├── poetry.lock
├── .gitignore
├── .env-example
└── README.md
```

## Testing

Run tests using pytest:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=api --cov=report --cov=db
```

## License

This project is licensed under the MIT License. Feel free to use, modify, and distribute.