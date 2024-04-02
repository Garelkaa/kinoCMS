from django.db import models


class Gallery(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)
    title = models.CharField(max_length=100)

    class Meta:
        db_table = 'gallery'
        verbose_name = 'Галерея'
        verbose_name_plural = 'Галереї'



class GalleryImage(models.Model):
    image = models.ImageField(verbose_name="Картинка галереї")
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, verbose_name="Галерея")

    class Meta:
        db_table = 'gallery_image'
        verbose_name = 'Картинка галереї'
        verbose_name_plural = 'Картинки галереї'
