FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    ffmpeg \
    wget \
    libx11-6 \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Download and install geckodriver
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-linux64.tar.gz && \
    tar -xvzf geckodriver-v0.34.0-linux64.tar.gz && \
    rm geckodriver-v0.34.0-linux64.tar.gz && \
    chmod +x geckodriver && \
    mv geckodriver /usr/local/bin/

RUN apt-get update && apt-get install -y wget bzip2 libxtst6 libgtk-3-0 libx11-xcb-dev libdbus-glib-1-2 libxt6 libpci-dev && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y firefox

WORKDIR /app

COPY ./POCs/docker-test.py /app/

ENTRYPOINT ["xvfb-run", "--", "python3", "docker-test.py"]