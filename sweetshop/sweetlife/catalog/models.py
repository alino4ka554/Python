from django.db import models
from django.urls import reverse

# Create your models here.
class InStockModel(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(in_stock=Dessert.Status.INSTOCK)


class Dessert(models.Model):
    class Status(models.IntegerChoices):
        OUTOFSTOCK = 0, 'Нет в наличии'
        INSTOCK = 1, 'В наличии'
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    in_stock = models.BooleanField(choices=Status.choices, default=Status.OUTOFSTOCK)
    image = models.ImageField(blank=True, null=True)
    slug = models.SlugField(max_length=255, db_index=True, unique=True)
    objects = models.Manager()
    stocked = InStockModel()
    def get_absolute_url(self):
        return reverse('cake', kwargs={'cake_slug': self.slug})
    def __str__(self):
        return self.title