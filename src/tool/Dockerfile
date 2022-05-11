FROM python:3.9.9-slim-buster

ENV CMD=
ENV COUNT=

COPY requirements.txt /

RUN pip3 install -r /requirements.txt

COPY main_cli.py /app/main_cli.py

WORKDIR /app

CMD ["sh", "-c", "python3 main_cli.py ${CMD} ${COUNT}"]