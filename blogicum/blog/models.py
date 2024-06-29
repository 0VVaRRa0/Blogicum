from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from core.models import BaseModel


User = get_user_model()

MAX_TITLE_LENGTH = 256
TITLE_DISPLAY_LIMIT = 10


class Category(BaseModel):
    title = models.CharField(
        max_length=MAX_TITLE_LENGTH, verbose_name='Заголовок'
    )
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        unique=True, verbose_name='Идентификатор',
        help_text=('Идентификатор страницы для URL; '
                   'разрешены символы латиницы, цифры, '
                   'дефис и подчёркивание.')
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return (
            self.title[:TITLE_DISPLAY_LIMIT] + '...'
            if len(self.title) > TITLE_DISPLAY_LIMIT
            else self.title
        )


class Location(BaseModel):
    name = models.CharField(
        max_length=MAX_TITLE_LENGTH, verbose_name='Название места'
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return (
            self.name[:TITLE_DISPLAY_LIMIT] + '...'
            if len(self.name) > TITLE_DISPLAY_LIMIT
            else self.name
        )


class Post(BaseModel):
    title = models.CharField(
        max_length=MAX_TITLE_LENGTH, verbose_name='Заголовок'
    )
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата и время публикации',
        help_text=('Если установить дату и время в будущем '
                   '— можно делать отложенные публикации.')
    )
    author = models.ForeignKey(
        User, verbose_name='Автор публикации', on_delete=models.CASCADE
    )
    location = models.ForeignKey(
        Location, verbose_name='Местоположение',
        on_delete=models.SET_NULL, blank=True, null=True
    )
    category = models.ForeignKey(
        Category, verbose_name='Категория',
        on_delete=models.SET_NULL, null=True
    )
    image = models.ImageField(
        'Изображение', upload_to='blog_images', blank=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return (
            self.title[:TITLE_DISPLAY_LIMIT] + '...'
            if len(self.title) > TITLE_DISPLAY_LIMIT
            else self.title
        )


class Comment(models.Model):
    author = models.ForeignKey(
        User, verbose_name='Автор', on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post, verbose_name='Пост', on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField('Текст комментария')

    class Meta:
        ordering = ['-created_at',]
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return (
            self.text[:TITLE_DISPLAY_LIMIT] + '...'
            if len(self.text) > TITLE_DISPLAY_LIMIT
            else self.text
        )
