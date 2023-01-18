import flask
import numpy as np
import psutil
import redis
from flask_app import cpu_service
from werkzeug.middleware import proxy_fix

app = flask.Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)

cpu_service.main()

app.wsgi_app = proxy_fix.ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

@app.route("/api/cpu/usage/", methods=['GET'])
def get_cpu_usage() -> int:
    """Returns CPU usage as percentage"""
    usage = float(r.get('usage'))
    return flask.jsonify({'usage': f'{usage:4.1f}'})

@app.route("/api/cpu/temp/", methods=['GET'])
def get_cpu_temp() -> int:
    """Returns temperature in celsius of CPU"""
    with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
        temp_mdeg = float(f.readline())
        temp = np.round(temp_mdeg / 1e3, 1)

    return flask.jsonify({'temp0': f'{temp:.1f}'})

@app.route("/", methods=['GET','POST'])
def hello():
    """Unused root route. nginx serves this route instead"""
    return "<h1 style='color:blue'>Hello There!</h1>"

@app.route('/codenames/api/', methods=['GET', 'POST'])
def codenames():
    pass