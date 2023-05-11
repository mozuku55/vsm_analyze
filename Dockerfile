FROM python:3.10-slim

RUN pip install --upgrade pip
WORKDIR /VSM


COPY requirements.txt /VSM
COPY createFig /VSM