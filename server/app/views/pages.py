from flask import Blueprint
from flask import render_template

pages_blueprint = Blueprint('pages_blueprint', __name__, url_prefix="", template_folder='../templates/', static_folder='static', static_url_path='../static/')

@pages_blueprint.route('/', methods=['GET'])
def mainpage():
    return render_template("index.html")
