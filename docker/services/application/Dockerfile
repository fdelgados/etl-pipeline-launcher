FROM python:3.9-slim-buster

ARG REQUIREMENTS_FILE=requirements.txt

EXPOSE 5000

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-pymysql \
    bash \
    bash-completion \
    vim

CMD /usr/local/bin/python -m pip install --upgrade pip

COPY requirements.txt /tmp/
COPY $REQUIREMENTS_FILE /tmp/
RUN pip install -r /tmp/$REQUIREMENTS_FILE

RUN mkdir -p /var/www/src
RUN mkdir -p /var/www/data/content
RUN mkdir -p /export/certs
RUN mkdir -p /log
COPY src/ /var/www/src

WORKDIR /var/www

COPY setup.py setup.py
RUN pip install -e ./

COPY tests/ tests/
COPY config/ config/
COPY bin/ bin/
CMD chmod a+x bin/run_workers.py
CMD chmod a+x bin/console.py

WORKDIR /var/www/src
