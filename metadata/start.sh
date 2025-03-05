#!/bin/bash

# TODO: currently the script removes existing containers and runs new ones
# TODO: find a better way if there exists one
docker rm -f mongodb
docker run -p 27017:27017 --network notification-service --name mongodb -d mongo:latest

docker rm -f metadata-service-container
docker run -p 9000:9000 --network notification-service --name metadata-service-container metadata-service
