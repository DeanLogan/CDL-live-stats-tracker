# Use an official Python runtime as a parent image
FROM python:3.12.2-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY db/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the database scripts into the container
COPY db/create-db.py .
COPY db/populate-db.py .

# Command to run the database creation and population scripts
CMD ["python", "create-db.py"]