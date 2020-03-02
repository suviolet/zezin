from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# pylint: disable=dangerous-default-value,wrong-import-position,unused-import
def create_app(settings_override={}):
    app = Flask(__name__)
    app.config.from_object('zezin.settings.Configuration')
    app.config.update(settings_override)

    db.init_app(app)

    return app


import zezin.models  # isort:skip
