FROM python:3.9-slim-buster

EXPOSE 5000

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-pymysql


COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

RUN mkdir -p /src
COPY src/ /src/
RUN pip install -e /src

COPY tests/ /tests/
COPY config/ /config/

WORKDIR /src

CMD flask run --host=0.0.0.0 --port=5000
