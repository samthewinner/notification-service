#!/bin/bash

if [ "$1" == "build" ]; then
    docker-compose build
fi

if [ "$1" == "run" ]; then
    docker-compose up -d
fi

if [ "$1" == "stop" ]; then
    docker-compose down
fi

if [ "$1" == "restart" ]; then
    docker-compose down
    docker-compose up -d
fi

if [ "$1" == "logs" ]; then
    docker-compose logs -f
fi

if [ "$1" == "killall" ]; then
    docker rm -f frontend
    docker rm -f metadata
    docker rm -f mongodb
    docker rm -f kafka
fi
