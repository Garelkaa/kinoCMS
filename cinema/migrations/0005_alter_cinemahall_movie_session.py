# Generated by Django 4.1.7 on 2024-04-23 17:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0004_rename_gallery_id_cinemahall_gallery_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cinemahall',
            name='movie_session',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cinema.moviesession'),
        ),
    ]
