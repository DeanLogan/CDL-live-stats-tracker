# Dockerfile for Node.js Kafka Consumer
FROM node:14-slim

# Set up working directory
WORKDIR /app

# Copy package.json and install dependencies
COPY /consumer/package.json .
RUN npm install

# Copy the Node.js consumer code into the container
COPY /consumer/server.mjs .

# Command to run the Node.js consumer
CMD ["node", "server.mjs"]
