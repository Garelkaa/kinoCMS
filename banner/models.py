from django.db import models


class MainBannerSettings(models.Model):
    speed = models.IntegerField(verbose_name="Скорость")
    active = models.BooleanField(verbose_name="Активно")

    class Meta:
        db_table = 'mainbannersettings'


class MainBanner(models.Model):
    image = models.ImageField(verbose_name="Картинка")
    url = models.CharField(max_length=512, verbose_name="Ссылка")
    text = models.CharField(max_length=100, verbose_name="Название")
    settings = models.ForeignKey(MainBannerSettings, on_delete=models.CASCADE)

    class Meta:
        db_table = 'mainbanner'


class NewsBannerSettings(models.Model):
    speed = models.IntegerField(verbose_name="Скорость")
    active = models.BooleanField(verbose_name="Активно")


class NewsBanner(models.Model):
    image = models.ImageField(verbose_name="Картинка")
    url = models.CharField(max_length=512, verbose_name="Ссылка")
    text = models.CharField(max_length=100, verbose_name="Название")
    settings = models.ForeignKey(NewsBannerSettings, on_delete=models.CASCADE)

    class Meta:
        db_table = 'newsbanner'


class BackBanner(models.Model):
    TYPE_CHOICE = {
        ('d', 'Default photo'),
        ('f', 'Fon photo',)
    }
    image = models.ImageField(verbose_name="Картинка")
    choice = models.CharField(max_length=1, verbose_name="", choices=TYPE_CHOICE, null=True, blank=True)
    status = models.BooleanField(default=True, verbose_name="Активно")

    class Meta:
        db_table = 'backbanners'
