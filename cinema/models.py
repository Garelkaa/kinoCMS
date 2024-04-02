from django.utils import timezone

from django.db import models

from gallery.models import Gallery
from users.models import CustomUser
from banner.models import MainBanner


class Cinema(models.Model):
    title = models.CharField(max_length=50)
    created = models.DateTimeField(default=timezone.now)
    description = models.TextField(null=True, blank=True)
    main_image = models.ImageField(null=True)
    top_image = models.ImageField(null=True)
    url_trailer = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    seo_url = models.TextField(null=True, blank=True)
    seo_title = models.TextField(null=True, blank=True)
    seo_keywords = models.TextField(null=True, blank=True)
    description_seo = models.TextField(null=True, blank=True)
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'cinema'
        verbose_name = 'Кинотеатр'
        verbose_name_plural = 'Кинотеатры'
    

class Movie(models.Model):
    TYPE_CHOICES = (
        ('3D', '3D'),
        ('2D', '2D'),
        ('IMAX', 'АйМакс'),
    )
    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(max_length=7000, verbose_name='Описание')
    main_image = models.ImageField(verbose_name='Картинка на главной')
    url_trailer = models.CharField(max_length=512, verbose_name='URL трейлер')
    type = models.CharField(max_length=4, choices=TYPE_CHOICES, verbose_name='Тип', null=True, blank=True)
    seo_url = models.TextField(null=True, blank=True)
    seo_title = models.TextField(null=True, blank=True)
    seo_keywords = models.TextField(null=True, blank=True)
    description_seo = models.TextField(null=True, blank=True)
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, verbose_name='Галлерея айди')
    
    class Meta:
        db_table = 'movie'
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'

class MovieSession(models.Model):
    time = models.TimeField(verbose_name='Время')
    price = models.IntegerField(verbose_name='Цена')
    date = models.DateField(verbose_name='Дата')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='Фильм')

    
    class Meta:
        db_table = 'moviesession'
        verbose_name = 'Сессия фыильма'
        verbose_name_plural = 'Сессия фильмов'

class CinemaHall(models.Model):
    number = models.IntegerField(verbose_name='Номер зала')
    description = models.TextField(verbose_name='Описание зала', default='')
    scheme_image = models.ImageField(default='-')
    create_at = models.DateTimeField(auto_now=True, verbose_name='Время создавания')
    top_image = models.ImageField(default='-', verbose_name='Топ баннер')
    seo_url = models.TextField(null=True, blank=True)
    seo_title = models.TextField(null=True, blank=True)
    seo_keywords = models.TextField(null=True, blank=True)
    description_seo = models.TextField(null=True, blank=True)
    gallery_id = models.OneToOneField(Gallery, on_delete=models.CASCADE, verbose_name='', default=None)
    movie_session_id = models.OneToOneField(MovieSession, on_delete=models.CASCADE, default=1)


    class Meta:
        db_table = 'cinemahall'
        verbose_name = 'Зал'
        verbose_name_plural = 'Залы'

class Ticked(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Айди пользователя')
    movie_session_id = models.ForeignKey(MovieSession, on_delete=models.CASCADE, verbose_name='Айди сессии фильма')
    
    class Meta:
        db_table = 'ticket'
        verbose_name = 'Билет'
        verbose_name_plural = 'Билеты'
