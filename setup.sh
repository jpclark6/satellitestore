#!/bin/bash

# show all output, exit after any error
set -x
set -e

# set up virtual environment
python -m venv venv

# download requirements
pip install -r requirements.txt

# set env var for flask
export FLASK_APP=asset_store

# run database migrations
alembic upgrade head

echo "Now type `flask run` to begin running the app locally"
