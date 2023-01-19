FROM python:3.10

ENV PIP_ROOT_USER_ACTION=ignore

RUN apt-get update && \
    apt-get install gcc libpcre3 libpcre3-dev --yes && \
    pip install uWSGI flask redis numpy Werkzeug

COPY *.py /app/
COPY uwsgi.ini /app/

WORKDIR /app/

ENTRYPOINT [ "uwsgi", "--ini", "uwsgi.ini" ]
