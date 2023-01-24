FROM ubuntu:jammy

ENV PIP_ROOT_USER_ACTION=ignore

RUN apt-get update && \
    apt-get install python3.10 python3-pip --yes && \
    apt-get install libiio0 libiio-dev libiio-utils libad9361-dev --yes

RUN pip install matplotlib pylibiio pyadi-iio redis scipy

RUN apt-get install avahi-daemon -y

COPY *.py /app/

WORKDIR /app/

ENTRYPOINT [ "python3", "pluto.py" ]
