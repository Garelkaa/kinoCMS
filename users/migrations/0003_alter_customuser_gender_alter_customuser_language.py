# Generated by Django 4.1.7 on 2024-04-07 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_customuser_address_alter_customuser_birthdate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='gender',
            field=models.CharField(blank=True, choices=[('m', 'Male'), ('f', 'Female')], max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='language',
            field=models.CharField(blank=True, choices=[('u', 'English'), ('r', 'Russian')], max_length=2, null=True),
        ),
    ]
