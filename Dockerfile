FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    ffmpeg \
    wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./POCs/docker-test.py /app/

COPY requirements.txt /app/

RUN pip3 install -r /app/requirements.txt

ENTRYPOINT ["python3", "docker-test.py"]
