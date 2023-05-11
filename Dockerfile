FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
WORKDIR /VSM

COPY requirements.txt /VSM/
RUN pip install -r requirements.txt
RUN 

COPY . /VSM/

CMD ["python", "createFig/main.py"]
