import os
import sys
import time
from datetime import datetime, timedelta

import django
import pytz
from django.db.transaction import atomic
from loguru import logger
from yookassa import Configuration

from scheduler.choices import YookassaTransactionStatusEnum
from settings import Config


def init_django():
    from scheduler.settings import DJANGO_DIR

    sys.path.append(DJANGO_DIR)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin_panel.settings")
    django.setup()


def find_processing_transactions():
    from subscription.models import Transaction
    from subscription.model_mixins import TransactionStatus

    processing_transactions = Transaction.objects.filter(status=TransactionStatus.PROCESSING)
    return processing_transactions


def get_payment_status_api(payment_id):
    from yookassa import Payment

    Configuration.account_id = Config.yookassa_account_id
    Configuration.secret_key = Config.yookassa_secret_key

    payment = Payment.find_one(payment_id)
    return payment


def set_subscription(transaction):
    from subscription.models import Subscription
    from subscription.model_mixins import TransactionStatus, SubscriptionStatus

    with atomic():
        transaction.paid = True

        transaction.status = TransactionStatus.PAID
        transaction.save()

        today = datetime.now(pytz.timezone('Europe/Moscow'))
        end_expired_subscription = (today + timedelta(days=transaction.plan.duration)).replace(minute=0, second=0)

        Subscription.objects.create(
            plan=transaction.plan,
            end_date=end_expired_subscription,
            status=SubscriptionStatus.ACTIVE,
            customer_id=transaction.customer_id,
            payment_id=transaction.session_id,
        )
        logger.info(f'for user: {transaction.customer_id} set subscription')


def is_transaction_need_cancel(payment_created_at):
    from dateutil import parser

    created_at = int(parser.parse(payment_created_at).timestamp())
    now_timestamp = int(datetime.now(pytz.timezone('Europe/Moscow')).timestamp())
    is_old_payment = (now_timestamp - created_at) > Config.cancel_time_yookassa_payment
    return is_old_payment


def main():
    transactions = find_processing_transactions()
    for transaction in transactions:
        payment = get_payment_status_api(transaction.session_id)

        if is_transaction_need_cancel(payment.created_at):
            from subscription.model_mixins import TransactionStatus

            transaction.status = TransactionStatus.DECLINED
            transaction.save()
            logger.info(f'cancelled transaction {transaction.id}, because old payment')
            continue

        if payment.status == YookassaTransactionStatusEnum.SUCCESS:
            set_subscription(transaction)


if __name__ == '__main__':
    init_django()

    logger.info('scheduler init and starting')
    while True:
        main()
        time.sleep(Config.app_delay)
