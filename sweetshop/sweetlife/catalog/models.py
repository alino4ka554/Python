from django.db import models
from django.urls import reverse


class InStockModel(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(in_stock=Dessert.Status.INSTOCK)


class Dessert(models.Model):
    class Status(models.IntegerChoices):
        OUTOFSTOCK = 0, 'Нет в наличии'
        INSTOCK = 1, 'В наличии'
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    in_stock = models.BooleanField(choices=Status.choices,
                                   default=Status.OUTOFSTOCK)
    image = models.ImageField(blank=True, null=True)
    slug = models.SlugField(max_length=255, db_index=True, unique=True)
    objects = models.Manager()
    stocked = InStockModel()
    category = models.ForeignKey('Category', on_delete=models.CASCADE,
                                 related_name='desserts')
    tags = models.ManyToManyField('TagDessert', blank=True, related_name='tags')



    def get_absolute_url(self):
        return reverse('cake', kwargs={'cake_slug': self.slug})
    
    def __str__(self):
        return self.title


class TagDessert(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug':
                                      self.slug})

    def __str__(self):
        return self.tag


class Category(models.Model):
    name = models.CharField(max_length=100,
                            db_index=True)
    slug = models.SlugField(max_length=255,
                            unique=True, db_index=True)

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})   

    def __str__(self):
        return self.name
    

class DessertInfo(models.Model):
    dessert = models.OneToOneField(Dessert, on_delete=models.CASCADE, related_name='info')
    ingredients = models.TextField(blank=True)
    calories = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.dessert.title
