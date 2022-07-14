FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /billing_admin
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY ./admin_panel .

RUN python manage.py collectstatic --no-input
CMD python manage.py migrate && gunicorn admin_panel.wsgi:application --bind 0.0.0.0:9000