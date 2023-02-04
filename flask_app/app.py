import flask
import numpy as np
from scipy import signal
from werkzeug.middleware import proxy_fix
from flask import request, g
import redis
from dotenv import load_dotenv
import pickle
import os

REDIS_PORT_DEFAULT = 6379

load_dotenv()
app = flask.Flask(__name__)

# I don't really understand this but the getting started guide recommended it
app.wsgi_app = proxy_fix.ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)


def get_redis() -> redis.Redis:
    """Returns Redis database connection object"""
    if "r" not in g:
        g.r = redis.Redis(
            host="redis",
            port=int(os.environ.get("REDIS_PORT", REDIS_PORT_DEFAULT)),
            db=0,
        )
    return g.r


@app.route("/api/cpu/usage/", methods=["GET"])
def get_cpu_usage() -> flask.Response:
    """Returns CPU usage as percentage"""
    usage_buffer = get_redis().get("usage")
    if usage_buffer:
        usage = pickle.loads(usage_buffer)["value"]
        return flask.jsonify({"usage": f"{usage:4.1f}"})
    else:
        return flask.jsonify({"usage": None})


@app.route("/api/sdr/spectrum/", methods=["GET"])
def get_sdr_spectrum() -> flask.Response:
    """Returns SDR Spectrum as a list of magnitudes"""
    n = request.args.get("n", default=1, type=int)
    data = get_db_spectrum(n)
    return flask.jsonify({"spectrum": data})


@app.route("/api/sdr/capture_time/", methods=["GET"])
def get_capture_time() -> flask.Response:
    """Returns SDR Spectrum as a list of magnitudes"""
    data_buffer = get_redis().get("capture_time")
    if data_buffer:
        data = pickle.loads(data_buffer)["value"]
        return flask.jsonify({"capture_t": data})
    else:
        return flask.jsonify({"capture_t": None})


@app.route("/", methods=["GET", "POST"])
def hello():
    """Unused root route. nginx serves this route instead"""
    return (
        "<h1 style='color:blue'>Hello There! If you're seeing this,"
        "the nginx proxy is not properly configured to serve the static"
        "folder and is instead forwarding all traffic to the Flask backend</h1>"
    )


@app.route("/codenames/api/", methods=["GET", "POST"])
def codenames():
    return ""


def get_db_spectrum(n):
    spectrum = []

    key = [
        "GWL_RTN_WIDE",
        "C_FWD_WIDE",
        "D_FWD_WIDE",
        "E_FWD_WIDE",
        "F_FWD_WIDE",
        "F_FWD_WIDE",
    ]

    for itr in range(n):
        db_data = get_redis().get(key[itr])
        if db_data:
            data = np.array(pickle.loads(db_data)["value"]) + 120
            spectrum.append(data.tolist())
        else:
            spectrum.append([0, 0, 0])
    return spectrum


def get_pluto_spectrum(n):
    spectrum = []

    data = pickle.loads(get_redis().get("spectrum"))["value"]
    _, data = 10 * np.log10(
        signal.welch(data, window=np.hamming(512).tolist(), detrend=False)
    )
    data: np.ndarray = np.fft.fftshift(data)

    data_low = pickle.loads(get_redis().get("spectrum_low"))["value"]
    _, data_low = 10 * np.log10(
        signal.welch(data_low, window=np.hamming(512).tolist(), detrend=False)
    )
    data_low: np.ndarray = np.fft.fftshift(data_low)

    for itr in range(n):
        if itr >= 3:
            spectrum.append(data.tolist())
        else:
            spectrum.append(data_low.tolist())

    return spectrum


def get_example_spectrum(n):
    spectrum = []
    for _ in range(n):
        n_win = 512
        n_data = n_win * 16
        n_sinc = 16
        f_filt = 0.25
        data = (1 / np.sqrt(2)) * np.random.normal(size=n_data) + 1j * (
            1 / np.sqrt(2)
        ) * np.random.normal(size=n_data)
        data = np.convolve(
            data,
            np.sinc(np.linspace(-n_sinc // 2, n_sinc // 2, round(n_sinc / f_filt))),
            "same",
        )
        data = data + 0.1 * (
            (1 / np.sqrt(2)) * np.random.normal(size=n_data) + 1j * (1 / np.sqrt(2))
        )
        _, data = 10 * np.log10(
            signal.welch(data, window=np.hamming(n_win).tolist(), detrend=False)
        )
        data: np.ndarray = np.fft.fftshift(data)
        spectrum.append(data.tolist())
    return spectrum
