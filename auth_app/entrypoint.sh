#!/bin/sh

while ! nc -z "$DB_HOST" "$DB_PORT"; do sleep 1; done;

flask db upgrade
python grpc_server/server.py&
gunicorn "auth:create_app()" -b 0.0.0.0:8080 -w 4

exec "$@"
