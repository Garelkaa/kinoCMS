from celery import shared_task
from django.core.mail import send_mail
from other.models import Spam


@shared_task
def send_spam_emails(email_template, recipients):
    spam_template = Spam.objects.get(file_name=email_template)
    for recipient in recipients:
        send_mail(
            subject='Тема вашего письма',
            message='Текст вашего письма',
            from_email='beshenlyteam@gmail.com',
            recipient_list=[recipient],
            html_message=spam_template.file.read().decode()
        )
