# Use an official Node.js runtime as a parent image
FROM node:18

# Set the working directory in the container
WORKDIR /app

# Copy the package.json and install dependencies
COPY frontend/package.json /app/
COPY frontend/package-lock.json /app/
RUN npm install

# Copy the frontend code into the container
COPY frontend /app

# Build the frontend
RUN npm run build

# Expose the port the app runs on
EXPOSE 3000

# Start the frontend
CMD ["npm", "start"]