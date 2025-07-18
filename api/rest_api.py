"""REST API entry point for the application.
This module initializes the Flask application, sets up the Swagger documentation,
and registers the API blueprint for version 1 of the API."""

from flask import Flask
from flasgger import Swagger

from api.v1.resources import api_bp as v1_bp

app = Flask(__name__)
swagger = Swagger(app, template_file="v1/docs/swagger_spec.yml")

app.register_blueprint(v1_bp, url_prefix="/api/v1")

if __name__ == "__main__":
    app.run(debug=True)
