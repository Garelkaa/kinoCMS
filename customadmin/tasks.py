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


@shared_task
def send_selected_users(email_template, selectedUsers):
    spam_template = Spam.objects.get(file_name=email_template)
    email_subject = 'Тема вашего письма'
    email_body = spam_template.file.read().decode()

    for recipient in selectedUsers:
        send_mail(
            subject=email_subject,
            message="Текст",
            from_email='beshenlyteam@gmail.com',
            recipient_list=[recipient],
            html_message=email_body  # Передаем HTML-тело письма
        )
