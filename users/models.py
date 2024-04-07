from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    GENDER_CHOICES = (
        ("m", "Male"),
        ("f", "Female"),
    )

    LANGUAGE_CHOICES = (
        ("u", "English"),
        ("r", "Russian")
    )

    second_name = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phoneNumber = models.CharField(max_length=13, null=True, blank=True)
    card = models.CharField(max_length=16, null=True, blank=True)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = "custom_users"


class EmailSender(models.Model):
    mail = models.FileField()
    count_of_mails = models.IntegerField()
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    email_template_id = models.ForeignKey('EmailTemplates', on_delete=models.CASCADE)

    class Meta:
        db_table = "EmailSender"


class EmailTemplates(models.Model):
    title = models.CharField(max_length=200)
    body = models.FileField()
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        db_table = "EmailTemplates"
