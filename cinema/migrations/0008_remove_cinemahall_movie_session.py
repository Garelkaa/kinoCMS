# Generated by Django 4.1.7 on 2024-05-07 17:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0007_movie_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cinemahall',
            name='movie_session',
        ),
    ]