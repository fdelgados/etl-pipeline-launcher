FROM python:3.9-slim-buster

EXPOSE 5000

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-pymysql


COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

RUN mkdir -p /src
RUN mkdir -p /export/certs
RUN mkdir -p /log
COPY src/ /src/
COPY setup.py /setup.py
RUN pip install -e ./

COPY tests/ /tests/
COPY config/ /config/

WORKDIR /src

CMD flask run --host=0.0.0.0 --port=5000
