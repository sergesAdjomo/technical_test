# Path: start.sh
#!/bin/bash

# Stop existing containers
echo "Stopping existing containers..."
docker-compose down

# Build/update the image
echo "Building/Updating the image..."
docker-compose build

# Start the application
echo "Starting the application..."
docker-compose up -d

# Wait for the application to start
echo "Waiting for the application to start..."
sleep 5

# Check if the application is running
if docker-compose ps | grep -q "running"; then
    echo "Application started! Go to http://127.0.0.1:8000"
else
    echo "Error: the application did not start correctly."
    docker-compose logs
fi