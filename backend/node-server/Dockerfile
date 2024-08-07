# Use an official Node.js runtime as a parent image
FROM node:18

# Set the working directory in the container
WORKDIR /app

# Copy the package.json and package-lock.json files and install dependencies
COPY backend/node-server/package.json /app/
COPY backend/node-server/package-lock.json /app/
RUN npm install

# Copy the node-server code into the container
COPY backend/node-server /app

# Expose the port the app runs on
EXPOSE 3000

# Start the node server
CMD ["node", "server.js"]