import smtplib
from datetime import datetime, timedelta

import pytz
from django.conf import settings
from django.core.mail import send_mail


from mailing.models import Mailing, Log


def send_mailing():

    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)
    mailings = Mailing.objects.filter(status__in=[Mailing.STARTED, Mailing.CREATED])

    for mailing in mailings:
        # Завершение рассылки, если достигли end_date
        if mailing.end_date and current_datetime >= mailing.end_date:
            mailing.status = Mailing.COMPLETED
            mailing.save()
            continue
        # Нужна ли рассылка в текущий момент времени
        if mailing.next_send_time and current_datetime >= mailing.next_send_time:
            mailing.status = Mailing.STARTED
            clients = mailing.clients.all()
            try:
                server_response = send_mail(
                    subject=mailing.message.title,
                    message=mailing.message.text,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client.email for client in clients],
                    fail_silently=False,
                )
                Log.objects.create(
                    status=Log.SUCCESS,
                    server_answer=server_response,
                    mailing=mailing,
                )
            except smtplib.SMTPException as ex:
                Log.objects.create(
                    status=Log.FAILED,
                    server_answer=str(ex),
                    mailing=mailing,
                )

            if mailing.periodicity == Mailing.DAILY:
                mailing.next_send_time = current_datetime + timedelta(days=1)
            elif mailing.periodicity == Mailing.WEEKLY:
                mailing.next_send_time = current_datetime + timedelta(days=7)
            elif mailing.periodicity == Mailing.MONTHLY:
                mailing.next_send_time = current_datetime + timedelta(days=30)

            mailing.save()
