# Generated by Django 4.1.7 on 2024-05-08 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banner', '0011_alter_backbanner_choice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='backbanner',
            name='choice',
            field=models.CharField(blank=True, choices=[('f', 'Fon photo'), ('d', 'Default photo')], max_length=1, null=True, verbose_name=''),
        ),
    ]
