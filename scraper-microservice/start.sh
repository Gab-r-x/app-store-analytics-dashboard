#!/bin/bash

# Init main.py + celery worker
python /app/src/main.py & \
exec celery -A tasks worker --loglevel=info -Q default,app_details
