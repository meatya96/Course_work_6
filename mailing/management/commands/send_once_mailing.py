import smtplib

from django.conf import settings
from django.core.mail import send_mail
from django.core.management import BaseCommand

from mailing.models import Mailing, Log


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        mailings = Mailing.objects.filter(status='Запущена')

        for mailing in mailings:
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
