from django.db import models

from gallery.models import Gallery


class News(models.Model):
    title = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)
    main_image = models.ImageField()
    url_trailer = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    seo_url = models.TextField(null=True, blank=True)
    seo_title = models.TextField(null=True, blank=True)
    seo_keywords = models.TextField(null=True, blank=True)
    description_seo = models.TextField(null=True, blank=True)
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)


class Promotions(models.Model):
    title = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)
    main_image = models.ImageField()
    url_trailer = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    seo_url = models.TextField(null=True, blank=True)
    seo_title = models.TextField(null=True, blank=True)
    seo_keywords = models.TextField(null=True, blank=True)
    description_seo = models.TextField(null=True, blank=True)
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)


class Pages(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    main_image = models.ImageField()
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    active = models.BooleanField(default=True)
    seo_url = models.TextField(null=True, blank=True)
    seo_title = models.TextField(null=True, blank=True)
    seo_keywords = models.TextField(null=True, blank=True)
    description_seo = models.TextField(null=True, blank=True)
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)


class MainPage(models.Model):
    phone_number = models.CharField(max_length=13)
    seo_text = models.TextField(null=True, blank=True)
    seo_url = models.TextField(null=True, blank=True)
    seo_title = models.TextField(null=True, blank=True)
    seo_keywords = models.TextField(null=True, blank=True)
    description_seo = models.TextField(null=True, blank=True)


class Spam(models.Model):
    file_name = models.CharField(max_length=50)
    file = models.FileField()
