#!/bin/bash

docker-compose up api database --build -d

pytest "${BASH_SOURCE%/*}" -rP

docker-compose down