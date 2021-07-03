FROM python:3.8


WORKDIR /article

ADD . /article/
COPY . /article/

RUN apt-get update \
    && apt-get install gcc libffi-dev -y \
    && apt-get clean

RUN pip install --no-cache-dir -r requirements.txt
