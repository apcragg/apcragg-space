import flask
import numpy as np
from scipy import signal
from werkzeug.middleware import proxy_fix
from flask import request
import redis
import pickle

app = flask.Flask(__name__)

app.wsgi_app = proxy_fix.ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

r = redis.Redis(host="redis", port=6379, db=0)


@app.route("/api/cpu/usage/", methods=["GET"])
def get_cpu_usage() -> flask.Response:
    """Returns CPU usage as percentage"""
    usage = pickle.loads(r.get("usage"))["value"]
    return flask.jsonify({"usage": f"{usage:4.1f}"})


@app.route("/api/cpu/temp/", methods=["GET"])
def get_cpu_temp() -> flask.Response:
    """Returns temperature in celsius of CPU"""
    # with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
    #     temp_mdeg = float(f.readline())
    #     temp = np.round(temp_mdeg / 1e3, 1)
    temp = np.random.normal() * 5 + 20

    return flask.jsonify({"temp0": f"{temp:.1f}"})


@app.route("/api/sdr/spectrum/", methods=["GET"])
def get_sdr_spectrum() -> flask.Response:
    """Returns SDR Spectrum as a list of magnitudes"""
    n = request.args.get("n", default=1, type=int)
    data = get_pluto_spectrum(n)
    return flask.jsonify({"spectrum": data})


@app.route("/", methods=["GET", "POST"])
def hello():
    """Unused root route. nginx serves this route instead"""
    return "<h1 style='color:blue'>Hello There!</h1>"


@app.route("/codenames/api/", methods=["GET", "POST"])
def codenames():
    return ""


def get_pluto_spectrum(n):
    spectrum = []

    data = pickle.loads(r.get("spectrum"))["value"]
    _, data = 10 * np.log10(
        signal.welch(data, window=np.hamming(512).tolist(), detrend=False)
    )
    data: np.ndarray = np.fft.fftshift(data)

    data_low = pickle.loads(r.get("spectrum_low"))["value"]
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
