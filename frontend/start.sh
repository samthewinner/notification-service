#!/bin/bash

docker rm -f frontend-service-container
docker run -it -p 8000:8000 --name frontend-service-container frontend-service