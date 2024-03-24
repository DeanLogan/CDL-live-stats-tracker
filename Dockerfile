# Use an image with X11 support
FROM dorowu/ubuntu-desktop-lxde-vnc:bionic

WORKDIR /app

RUN apt-get update && apt-get install -y python3 python3-pip tesseract-ocr

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python3", "./tesseract.py" ]

# docker run -e DISPLAY=host.docker.internal:0.0 your_image_name