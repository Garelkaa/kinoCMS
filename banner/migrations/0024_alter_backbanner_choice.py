# Generated by Django 5.0.6 on 2024-06-04 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banner', '0023_alter_backbanner_choice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='backbanner',
            name='choice',
            field=models.CharField(blank=True, choices=[('f', 'Fon photo'), ('d', 'Default photo')], max_length=1, null=True, verbose_name=''),
        ),
    ]
