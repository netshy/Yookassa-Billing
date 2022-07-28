FROM python:3.9.12

ARG UNAME=scheduler
ARG APP_DIR=/transactions_scheduler

RUN apt-get update && apt-get -y upgrade && apt install -y netcat

WORKDIR $APP_DIR
COPY scheduler/requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

RUN useradd -b $APP_DIR -U $UNAME

USER $UNAME
COPY --chown=$UNAME:$UNAME scheduler/ ./scheduler
COPY --chown=$UNAME:$UNAME billing_admin_panel/ ./billing_admin_panel

EXPOSE 8080
ENV PYTHONPATH $APP_DIR
ENTRYPOINT ["sh","./scheduler/entrypoint.sh"]
