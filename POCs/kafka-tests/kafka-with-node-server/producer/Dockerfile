# Dockerfile for Python Kafka Producer
FROM python:3.12.2-slim

# Set up working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY /producer/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python producer code into the container
COPY /producer/producer.py .

# Command to run the Python producer
CMD ["python", "producer.py"]
