import psycopg2
from psycopg2 import extensions
import time
import threading
import queue
import logging
from typing import Optional, List


class DataStreamer(threading.Thread):
    """
    DataStreamer is a thread class that continuously queries a PostgreSQL database
    for new rows in a specified table and sends any previously unseen rows to a
    user-defined function for processing.

    The thread connects to a specified database, executes a query for new data,
    and waits for a specified interval before executing the next query. If a
    connection issue occurs, the thread will attempt to reconnect to the database.
    """

    def __init__(
        self,
        database: str,
        user: str,
        password: str,
        host: str,
        port: str,
        data_queue: queue.Queue,
        query_interval: int = 1,
        log_level: int = logging.DEBUG,
    ):
        """
        Initializes a new instance of the `DataStreamer` class.

        Args:
            database (str): The name of the database.
            user (str): The username for connecting to the database.
            password (str): The password for connecting to the database.
            host (str): The host address of the database.
            port (int): The port of the database.
            _process_new_data (callable): A user-defined function for processing new
                data.
            query_interval (int, optional): The number of seconds to wait before
                executing the next query. Defaults to 1.
        """
        super().__init__()
        self.conn: Optional[extensions.connection] = None
        self.cur: Optional[extensions.cursor] = None
        self.database: str = database
        self.user: str = user
        self.password: str = password
        self.host: str = host
        self.port: str = port
        self.data_queue: queue.Queue[List] = data_queue
        self.query_interval: int = query_interval
        self.logger: logging.Logger = logging.getLogger()
        self.logger.setLevel(log_level)
        logging.basicConfig()
        self.last_rec_index: int = -1
        self.stopped: bool = False
        self.exception: Optional[Exception] = None

    def run(self):
        self.logger.info("DataStreamer started")
        while not self.stopped:
            try:
                if not self.conn or self.conn.closed:
                    self._connect()
                self._query_data()
            except Exception as e:
                self.exception = e
                self.logger.exception("Error while querying data")
                self._disconnect()
            time.sleep(self.query_interval)
        self.logger.info("DataStreamer stopped")

    def _connect(self):
        self.logger.debug("Connecting to database")
        self.conn = psycopg2.connect(
            database=self.database,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
        )
        self.cur = self.conn.cursor()
        self.logger.debug("Connected to database")

    def _query_data(self):
        query = f"""
            SELECT rec_index, source_time, carrier, eirp, trace
            FROM tlm_ground_segment_monics_telemetry
            WHERE rec_index > {self.last_rec_index}
            AND source_time > NOW() - INTERVAL '1 MINUTE'
            ORDER BY rec_index;
        """
        if self.cur is None:
            self.logger.error("Called query data on closed connection")
            return
        time.sleep(1)
        self.cur.execute(query)
        data = self.cur.fetchall()

        for row in data:
            rec_index, *other_columns = row
            if rec_index > self.last_rec_index:
                self.last_rec_index = rec_index
                self._process_new_data(other_columns)

    def _process_new_data(self, new_data):
        # TODO: Error Handling
        self.data_queue.put(new_data)

    def _disconnect(self):
        self.logger.debug("Disconnecting from database")
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
        self.logger.debug("Disconnected from database")

    def get_qsize(self) -> int:
        return self.data_queue.qsize()

    def read_queue(self) -> List:
        # TODO: Error Handling
        return self.data_queue.get()

    def stop(self):
        self.stopped = True

    def has_exception(self):
        return self.exception
