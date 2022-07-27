FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /worker
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY src .

CMD python -m gunicorn main:app -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000