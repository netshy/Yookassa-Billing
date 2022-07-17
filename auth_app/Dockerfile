FROM python:3.9.12

ARG UNAME=auth
ARG APP_DIR=/auth

RUN apt-get update && apt-get -y upgrade && apt install -y netcat

WORKDIR $APP_DIR
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

RUN useradd -b $APP_DIR -U $UNAME

USER $UNAME
COPY --chown=auth:auth ./ .
COPY --chown=auth:auth ./entrypoint.sh .

EXPOSE 8080

ENTRYPOINT ["sh","./entrypoint.sh"]
