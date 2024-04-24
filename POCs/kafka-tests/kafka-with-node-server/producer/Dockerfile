# Dockerfile for Python Kafka Producer
FROM python:3.12.2-slim

# Set up working directory
WORKDIR /app

# Install curl
RUN apt-get update && apt-get install -y curl

# Copy the requirements file and install dependencies
COPY /producer/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python producer code into the container
COPY /producer/producer.py .

# Copy the wait for kafka command that will be used to wait for the kafka broker to be ready
# COPY /wait-for-kafka.sh .
# RUN chmod +x ./wait-for-kafka.sh

# Command to run the waiting script and the Python producer
ENTRYPOINT ["python", "-u", "producer.py"]
