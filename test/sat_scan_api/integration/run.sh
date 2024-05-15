#!/bin/bash

docker-compose up api database --build -d

pytest "${BASH_SOURCE%/*}" -x -rP

# Capture the exit status
pytest_status=$?

docker-compose down

if [ $pytest_status -eq 0 ]; then
  echo "✅ Integration Tests Pass"
  exit 0
else
  echo "🚨 Integration Test Failure"
  exit 1
fi