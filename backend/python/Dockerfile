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
    tesseract-ocr \
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

COPY game-stats-recorder.py /app/

COPY requirements.txt /app/

COPY uBlock0_1.56.1rc5.firefox.signed.xpi /app/

RUN python3 -m pip install -r /app/requirements.txt

ENTRYPOINT ["/bin/bash"]

# xvfb-run -- game-stats-recorder.py