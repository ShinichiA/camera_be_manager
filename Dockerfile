FROM python:3.7.9-alpine3.12

WORKDIR /app
COPY . /app/
RUN rm -rf /app/venv/
RUN python -m pip install --upgrade pip
RUN apk add --no-cache --virtual build-dependencies gcc libc-dev build-base git bash libffi-dev openssl-dev mariadb-connector-c-dev
RUN pip install -U --no-cache-dir -r requirements.txt
