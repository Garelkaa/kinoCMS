from celery import shared_task
from celery_progress.backend import ProgressRecorder  # Импортируем ProgressRecorder
from django.core.mail import send_mail
from other.models import Spam

@shared_task(bind=True)  # Добавляем bind=True для доступа к self
def send_spam_emails(self, email_template, recipients):
    spam_template = Spam.objects.get(file_name=email_template)
    progress_recorder = ProgressRecorder(self)  # Создаем экземпляр ProgressRecorder

    # Определяем общее количество писем для отправки
    total_emails = len(recipients)
    emails_sent = 0

    for recipient in recipients:
        send_mail(
            subject='Тема вашего письма',
            message='Текст вашего письма',
            from_email='beshenlyteam@gmail.com',
            recipient_list=[recipient],
            html_message=spam_template.file.read().decode()
        )
        emails_sent += 1
        progress_recorder.set_progress(emails_sent, total_emails)  # Устанавливаем прогресс

    return {'total': total_emails, 'sent': emails_sent}  # Возвращаем общее количество и количество отправленных писем

@shared_task(bind=True)
def send_selected_users(self, email_template, selectedUsers):
    spam_template = Spam.objects.get(file_name=email_template)
    progress_recorder = ProgressRecorder(self)

    total_emails = len(selectedUsers)
    emails_sent = 0

    email_subject = 'Тема вашего письма'
    email_body = spam_template.file.read().decode()

    for recipient in selectedUsers:
        send_mail(
            subject=email_subject,
            message="Текст",
            from_email='beshenlyteam@gmail.com',
            recipient_list=[recipient],
            html_message=email_body
        )
        emails_sent += 1
        progress_recorder.set_progress(emails_sent, total_emails)
        
    return True
