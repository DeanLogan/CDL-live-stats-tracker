#!/bin/bash

# Install kcat
apt-get update && apt-get install -y kcat

# Wait for Kafka to be ready
until kcat -b kafka:9092 -t test -C -e -q; do
    printf ''
    sleep 10
done
printf "Kafka is ready!\n"

echo "Executing command: $@"

# Start the application
exec "$@"