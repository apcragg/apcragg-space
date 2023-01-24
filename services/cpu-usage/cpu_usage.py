import threading
import time

import psutil
import redis
import pickle

N_THREADS = 1


def read_cpu_usage() -> None:
    r = redis.Redis(host="redis", port=6379, db=0)
    while True:
        usage = psutil.cpu_percent(0.0)
        if usage == 0.0:
            pass
        r.set("usage", pickle.dumps({"value": usage}))
        time.sleep(1)


def main():
    for n in range(N_THREADS):
        thread = threading.Thread(target=read_cpu_usage)
        thread.start()


if __name__ == "__main__":
    main()
