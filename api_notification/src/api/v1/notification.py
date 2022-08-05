import http

from fastapi import APIRouter
from loguru import logger
from pika.exceptions import UnroutableError
from starlette.exceptions import HTTPException
from starlette.responses import Response

import broker
from api.config import config

from models.choices import NotificationType
from models.email_event import EmailEvent, EmailNotificationBody
from models.payment_event import PaymentEvent, UserPaymentNotification

router = APIRouter()


@router.post("/send_notification", status_code=http.HTTPStatus.CREATED)
async def send_notification_event(body: EmailNotificationBody):
    event = EmailEvent(
        data=body.data,
        is_advertisement=body.is_advertisement,
        template_id=body.template_id,
        type=body.type,
        subject=body.subject,
    )

    try:
        broker.rabbitmq_broker.basic_publish(event)
    except UnroutableError:
        logger.error("message was returned")
        raise HTTPException(status_code=http.HTTPStatus.NOT_FOUND)
    except Exception as err:
        logger.error(f"publish error: {str(err)}")
        raise HTTPException(status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    return Response(status_code=201)


@router.post("/payment_notification", status_code=http.HTTPStatus.CREATED)
async def publish_payment_event_to_queue(request: UserPaymentNotification):
    if request.is_success:
        template_id = config.payment_ok_template_id
    else:
        template_id = config.payment_fail_template_id

    event = PaymentEvent(
        is_advertisement=False,
        template_id=template_id,
        user_id=str(request.user_id),
        type=NotificationType.payment_email,
    )

    try:
        broker.rabbitmq_broker.basic_publish(event)
    except UnroutableError:
        logger.error("message was returned")
        raise HTTPException(status_code=http.HTTPStatus.NOT_FOUND)
    except Exception as err:
        logger.error(f"publish error: {str(err)} | user_id: {request.user_id}")
        raise HTTPException(status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    return Response(status_code=201)


@router.post("/refund_notification", status_code=http.HTTPStatus.CREATED)
async def publish_refund_event_to_queue(request: UserPaymentNotification):
    event = PaymentEvent(
        is_advertisement=False,
        template_id=config.payment_refund_ok_template_id,
        user_id=str(request.user_id),
        type=NotificationType.payment_email,
    )

    try:
        broker.rabbitmq_broker.basic_publish(event)
    except UnroutableError:
        logger.error("message was returned")
        raise HTTPException(status_code=http.HTTPStatus.NOT_FOUND)
    except Exception as err:
        logger.error(f"publish error: {str(err)} | user_id: {request.user_id}")
        raise HTTPException(status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    return Response(status_code=201)
