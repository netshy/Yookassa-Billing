#!/bin/sh

while ! nc -z "$DB_HOST" "$DB_PORT"; do sleep 1; done;

python scheduler/main.py

exec "$@"
