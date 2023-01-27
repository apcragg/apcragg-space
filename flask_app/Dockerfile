FROM python:3.10

RUN apt-get update && \
    apt-get install gcc libpcre3 libpcre3-dev iputils-ping --yes && \
    pip install uWSGI flask redis numpy Werkzeug scipy python-dotenv

COPY *.py /app/
COPY uwsgi.ini /app/

WORKDIR /app/

ENTRYPOINT uwsgi --ini uwsgi.ini --socket 0.0.0.0:$FLASK_BACKEND_PORT
