# Generated by Django 4.1.7 on 2024-04-17 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banner', '0004_alter_backbanner_choice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='backbanner',
            name='choice',
            field=models.CharField(blank=True, choices=[('d', 'Default photo'), ('f', 'Fon photo')], max_length=1, null=True, verbose_name=''),
        ),
    ]
