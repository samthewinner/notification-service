#!/bin/bash

# TODO: currently the script removes existing containers and runs new ones
# TODO: find a better way if there exists one
docker run --rm -p 8000:8000 --network notification-service --name frontend-service-container frontend-service
