FROM python:3.10-slim

RUN apt-get update && \
    apt-get install gcc libpcre3 libpcre3-dev --yes && \
    pip install psutil redis
COPY *.py /app/
WORKDIR /app/

ENTRYPOINT [ "python3", "cpu_usage.py" ]
