FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /billing_admin

RUN apt-get update && apt-get -y upgrade && apt install -y netcat

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY ./admin_panel .

ENTRYPOINT ["sh","./entrypoint.sh"]