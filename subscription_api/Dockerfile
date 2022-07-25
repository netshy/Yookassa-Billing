FROM python:3.8

ARG APP_DIR=/subscription_api
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=$APP_DIR

WORKDIR $APP_DIR
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY src .

CMD python -m gunicorn main:app -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000