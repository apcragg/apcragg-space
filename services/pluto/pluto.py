import adi
import numpy as np
import redis
import pickle

N_THREADS = 1


def find_sdr():
    return "usb:1.3.5"


def setup_sdr(uri: str):
    sdr = adi.Pluto(uri=uri)
    return sdr


def main():
    sdr_uri = find_sdr()
    sdr = setup_sdr(uri=sdr_uri)
    sdr.rx_buffer_size = 1024 * 8
    sdr.sample_rate = int(30.72e6)
    sdr.rx_rf_bandwidth = int(30.72e6)
    sdr.rx_lo = int(751e6)
    sdr.gain_control_mode_chan0 = "manual"
    sdr.rx_hardwaregain_chan0 = 70.0

    r = redis.Redis(host="redis", port=6379, db=0)

    while True:
        sdr.rx_lo = int(751e6)
        data = sdr.rx() / (2**12)
        spectrum = data
        r.set("spectrum", pickle.dumps({"value": spectrum}))

        sdr.rx_lo = int(433e6)
        data = sdr.rx() / (2**12)
        spectrum = data
        r.set("spectrum_low", pickle.dumps({"value": spectrum}))


if __name__ == "__main__":
    main()
