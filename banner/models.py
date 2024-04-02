from django.db import models


class MainBannerSettings(models.Model):
    speed = models.IntegerField(verbose_name="Скорость")
    active = models.BooleanField(verbose_name="Активно")

    class Meta:
        db_table = 'MainBannerSettings'


class MainBanner(models.Model):
    image = models.ImageField(verbose_name="Картинка")
    url = models.CharField(max_length=512, verbose_name="Ссылка")
    text = models.CharField(max_length=100, verbose_name="Название")
    settings = models.ForeignKey(MainBannerSettings, on_delete=models.CASCADE)

    class Meta:
        db_table = 'MainBanner'


class NewsBannerSettings(models.Model):
    speed = models.IntegerField(verbose_name="Скорость")
    active = models.BooleanField(verbose_name="Активно")


class NewsBanner(models.Model):
    image = models.ImageField(verbose_name="Картинка")
    url = models.CharField(max_length=512, verbose_name="Ссылка")
    text = models.CharField(max_length=100, verbose_name="Название")
    settings = models.ForeignKey(NewsBannerSettings, on_delete=models.CASCADE)

    class Meta:
        db_table = 'NewsBanner'


class BackBanner(models.Model):
    image = models.ImageField(verbose_name="Картинка")
    choice = models.CharField(max_length=1, verbose_name="Вибір якийсь")

    class Meta:
        db_table = 'BackBanners'
