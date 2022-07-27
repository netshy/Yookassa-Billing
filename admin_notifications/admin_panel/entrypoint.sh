#!/bin/sh

while ! nc -z "$DB_HOST" "$DB_PORT"; do sleep 1; done;

python manage.py collectstatic --no-input

python manage.py migrate
python manage.py loaddata fixtures/fixture.json
python -m gunicorn admin_panel.wsgi:application --bind 0.0.0.0:9000

exec "$@"
