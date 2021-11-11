import threading
import flask
from flask import Blueprint, make_response, jsonify
import time
import RPi.GPIO as GPIO

from app import GetRowVals, GetTimestamp
from app.models import db, SensorEntry


capture_blueprint = Blueprint('capture', __name__, url_prefix="/capture")

def get_thread_by_name(name):
    threads = threading.enumerate()
    for thread in threads:
        if thread.getName() == name:
            return thread
    return None

class CaptureThread(threading.Thread):
    def __init__(self, app, input_pin):
        self.app = app

        self.input_pin = input_pin

        threading.Thread.__init__(self)
        self.stopRequest = False

    def run(self):
        print("====== Capture Thread (%d) started!" % self.input_pin)
        with self.app.app_context():
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.input_pin, GPIO.IN)

            while not self.stopRequest:
                current_value = GPIO.input(self.input_pin)
                last_entry = db.session.query(SensorEntry).filter(SensorEntry.gpio == "%d"%self.input_pin).order_by(SensorEntry.id.desc()).first()

                if last_entry is not None:
                    last_value = last_entry.value
                else:
                    last_value = None

                if last_value is None or current_value != last_value:
                    # insert last value again so it looks nicer in the graph
                    if last_value is not None:
                        db.session.add(
                            SensorEntry(
                                gpio="%d"%self.input_pin,
                                timestamp=GetTimestamp()-1,
                                value=last_value)
                                )


                    db.session.add(
                        SensorEntry(
                            gpio="%d"%self.input_pin,
                            timestamp=GetTimestamp(),
                            value=current_value)
                            )
                    db.session.commit()
                else:
                    time.sleep(.001)

            print("==== Capture Thread (%d) stopped" % self.input_pin)

    def stop(self):
        self.stopRequest = True



@capture_blueprint.route('/', methods=['GET'])
def values():
    ret = []
    for input_pin in range(41):
        ret_i = []
        ses = SensorEntry.query.filter(SensorEntry.gpio == "%d"%input_pin).order_by(SensorEntry.id.desc()).limit(1000)
        for se in ses:
            ret_i.append(GetRowVals(se))
        ret.append(ret_i)
    return make_response(jsonify(ret), 200)

@capture_blueprint.route('/start/<int:input_pin>', methods=['GET'])
def start(input_pin):
    thr = CaptureThread(flask.current_app._get_current_object(), input_pin)
    thr.daemon = True
    thr.name = "%d" % input_pin
    thr.start()

    return make_response(jsonify({'msg':'OK'}),200)

@capture_blueprint.route('/stop/<int:input_pin>', methods=['GET'])
def stop(input_pin):
    thread = get_thread_by_name("%d"%input_pin)
    if thread:
        thread.stop()
        return make_response(jsonify({'msg':'OK'}),200)
    else:
        return make_response(jsonify({'msg':'Thread not found'}),404)

@capture_blueprint.route('/status', methods=['GET'])
def status():
    ret = []

    for input_pin in range(41):
        thread = get_thread_by_name("%d" % input_pin)
        if thread:
            ret.append({'status':1})
        else:
            ret.append({'status':0})

    return make_response(jsonify(ret))

@capture_blueprint.route('/reset/<int:input_pin>', methods=['GET'])
def reset(input_pin):
    SensorEntry.query.filter(SensorEntry.gpio == "%d" %input_pin).delete()
    db.session.commit()

    return make_response(jsonify({'msg':'OK'}),200)
