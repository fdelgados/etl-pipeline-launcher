FROM python:3.9.9 AS compile-image

RUN mkdir -p /opt/code
WORKDIR /opt/code

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    python3-pymysql

RUN python3 -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

RUN pip3 install --upgrade pip setuptools wheel

RUN pip3 install uwsgi==2.0.20

COPY requirements.txt /opt/

RUN pip3 install -r /opt/requirements.txt

RUN mkdir -p /opt/code/src
RUN mkdir -p /opt/code/tests
RUN mkdir -p /opt/code/config
RUN mkdir -p /opt/code/bin
RUN mkdir -p /opt/code/log
RUN mkdir -p /opt/code/data
RUN mkdir -p /opt/code/export/certs

COPY src/ /opt/code/src

COPY setup.py /opt/code/
RUN pip3 install -e /opt/code/

#############

FROM python:3.9.9 AS runtime-image

RUN apt-get update && apt-get install -y curl build-essential

RUN mkdir -p /opt/uwsgi
ADD docker/uwsgi.ini /opt/uwsgi/
ADD docker/start_server.sh /opt/uwsgi/

RUN addgroup --system uwsgi
RUN adduser --no-create-home --disabled-password --system uwsgi
USER uwsgi

COPY --chown=uwsgi:uwsgi --from=compile-image /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY --chown=uwsgi:uwsgi src/ /opt/code/src
COPY --chown=uwsgi:uwsgi tests/ /opt/code/tests
COPY --chown=uwsgi:uwsgi config/ /opt/code/config
COPY --chown=uwsgi:uwsgi bin/ /opt/code/bin
COPY --chown=uwsgi:uwsgi wsgi.py /opt/code

WORKDIR /opt/code
EXPOSE 5000
EXPOSE 8000

CMD ["/bin/sh", "/opt/uwsgi/start_server.sh"]
