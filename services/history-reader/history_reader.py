import time
import db_streamer
import logging
import queue
import os
import signal
from typing import Optional
import functools
import redis
import pickle

db_name = os.environ.get("DB_NAME", "")
db_user = os.environ.get("DB_USER", "")
db_pass = os.environ.get("DB_PASS", "")
db_host = os.environ.get("DB_HOST", "")
db_port = os.environ.get("DB_PORT", "")


def main():
    r = redis.Redis(host="redis", port=6379, db=0)
    streamer: Optional[db_streamer.DataStreamer] = None
    data_queue = queue.Queue()
    stopped = {"state": False}

    def signal_handler(_closure, sig, frame):
        _closure["state"] = True
        print("")
        logging.warning("Stopping data streamer")
        if streamer:
            streamer.stop()
        logging.warning("Stopped data streamer")
        return

    signal.signal(signal.SIGINT, functools.partial(signal_handler, stopped))

    settings = {
        "database": db_name,
        "user": db_user,
        "password": db_pass,
        "host": db_host,
        "port": db_port,
        "data_queue": data_queue,
    }
    streamer = db_streamer.DataStreamer(**settings)
    streamer.start()
    logging.info("Data Streamer started")

    while True and not stopped["state"]:
        data = streamer.read_queue()
        logging.info(
            f"Received new data from: {data[1]} -- "
            f"Queue Size: {streamer.get_qsize()}"
        )
        r.set(data[1], pickle.dumps({"value": data[3]}))
        logging.error(data[1])
        time.sleep(0.001)

    streamer.join()
    logging.info("Exiting program")


if __name__ == "__main__":
    main()
