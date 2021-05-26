import os

from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if not test_config:
        os.environ["SQLITE_URL"] = "sqlite:///database/db.db"
    else:
        os.environ["SQLITE_URL"] = test_config["SQLITE_URL"]

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import api

    app.register_blueprint(api.bp)

    return app
