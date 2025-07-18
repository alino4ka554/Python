from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model


class InStockModel(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(in_stock=Dessert.Status.INSTOCK)


class Dessert(models.Model):
    class Status(models.IntegerChoices):
        OUTOFSTOCK = 0, 'Нет в наличии'
        INSTOCK = 1, 'В наличии'
    class Meta:
        verbose_name = 'Десерт'
        verbose_name_plural = 'Десерты'
    title = models.CharField(max_length=255, verbose_name="Название")
    content = models.TextField(blank=True, verbose_name="Описание")
    in_stock = models.BooleanField(choices=tuple(map(lambda x:
                                (bool(x[0]), x[1]), Status.choices)),
                                   default=Status.OUTOFSTOCK,
                                   verbose_name="Статус")
    image = models.ImageField(blank=True, null=True,
                              upload_to="images/%Y/%m/%d/",
                              verbose_name="Изображение")
    slug = models.SlugField(max_length=255, db_index=True, unique=True,
                            verbose_name="Слаг")
    objects = models.Manager()
    stocked = InStockModel()
    price = models.IntegerField(default=0,
                                verbose_name="Цена")
    category = models.ForeignKey('Category', on_delete=models.CASCADE,
                                 related_name='desserts',
                                 verbose_name="Категория")
    tags = models.ManyToManyField('TagDessert', blank=True,
                                  related_name='tags',
                                  verbose_name="Теги")



    def get_absolute_url(self):
        return reverse('cake', kwargs={'cake_slug': self.slug})
    
    def __str__(self):
        return self.title

class Like(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='likes')
    dessert = models.ForeignKey(Dessert, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
        unique_together = ('user', 'dessert')

    def __str__(self):
        return f'{self.user.username} likes {self.dessert.title}'

class TagDessert(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug':
                                      self.slug})

    def __str__(self):
        return self.tag


class Category(models.Model):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    name = models.CharField(max_length=100,
                            db_index=True, verbose_name='Название')
    slug = models.SlugField(max_length=255,
                            unique=True, db_index=True,
                            verbose_name='Слаг')

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
    

class Comment(models.Model):
    text = models.TextField(verbose_name='Текст')
    dessert = models.ForeignKey(
        Dessert,
        on_delete=models.CASCADE,
        verbose_name='Комментарий',
        related_name='comments'
    )
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL,
                               related_name='comments', null=True, default=None)
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарий'
        ordering = ('created_at',)

    def __str__(self) -> str:
        text = str(self.text)
        return text[:20]

class Feedback(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='feedbacks')
    message = models.TextField(verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']

    def __str__(self):
        return f'Отзыв от {self.user.username} от {self.created_at.strftime("%d.%m.%Y")}' 