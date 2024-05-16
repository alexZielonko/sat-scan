#!/bin/bash

docker-compose up -d api database

# Wait for database to create/mount volume
sleep 10

alembic upgrade head

pytest "${BASH_SOURCE%/*}" -x -rP

# Capture the exit status
pytest_status=$?

docker-compose down

if [ $pytest_status -eq 0 ]; then
  echo "✅ [run.sh] Integration Tests Pass"
  exit 0
else
  echo "🚨 [run.sh] Integration Test Failure"
  exit 1
fi