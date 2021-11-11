from . import db
import datetime

class SensorEntry(db.Model):
    __tablename__ = 'sensorentry'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gpio = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Integer, nullable=False)
