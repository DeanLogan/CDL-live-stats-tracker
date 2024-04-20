# Dockerfile for Node.js Kafka Consumer
FROM node:14-slim

# Install netcat, required by wait-for-it.sh
RUN apt-get update && apt-get install -y netcat

# Set up working directory
WORKDIR /app

# Copy package.json and install dependencies
COPY /consumer/package.json .
RUN npm install

# Copy the Node.js consumer code into the container
COPY /consumer/server.mjs .

# Copy the wait-for-it.sh script into the container
COPY /wait-for-it.sh .
RUN chmod +x wait-for-it.sh

# Command to run the Node.js consumer
CMD ["./wait-for-it.sh", "kafka:9092", "--", "node", "server.mjs"]