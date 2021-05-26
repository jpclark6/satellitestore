#!/bin/bash

echo "Setting up virtual environment"
python -m venv venv
source venv/bin/activate

echo "Downloading and installing requirements"
pip install -r requirements.txt

# set env var required for flask
export FLASK_APP=asset_store

echo "Running migrations"
alembic upgrade head

echo "Running tests"
pytest

echo "Adding fake data to database"
python database/add_random_data.py

echo
echo "To start the flask app run 'flask run' to begin running the app locally"
