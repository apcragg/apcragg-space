FROM ubuntu:jammy

ENV PIP_ROOT_USER_ACTION=ignore

RUN apt-get update && \
    apt-get install libpq-dev python3.10 python3-pip --yes

RUN pip install pyadi-iio redis scipy psycopg2

COPY *.py /app/

WORKDIR /app/

ENTRYPOINT [ "python3", "history_reader.py" ]
