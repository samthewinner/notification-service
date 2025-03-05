#!/bin/bash

# TODO: currently the script removes existing containers and runs new ones
# TODO: find a better way if there exists one
docker rm -f frontend-service-container
docker run -p 8000:8000 --network notification-service --name frontend-service-container frontend-service