from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import date, datetime
import time

db = SQLAlchemy()

def GetRowVals(row, exclude=["_sa_instance_state"]):
    row_vals = {}
    for k,v in row.__dict__.items():
        if not k.startswith("_") and not k in exclude:
            if isinstance(v,date):
                row_vals[k] = v.strftime("%-d/%-m/%Y")
            else:
                row_vals[k] = v
    return row_vals

def GetTimestamp():
    #return int(datetime.timestamp(datetime.now()))
    return round(time.time()*1000)

def create_app():
    from .import models
    from .views.pages import pages_blueprint
    from .views.capture import capture_blueprint

    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    CORS(app)

    db.init_app(app)

    app.register_blueprint(pages_blueprint)
    app.register_blueprint(capture_blueprint)

    with app.app_context():
        db.create_all()

        return app
