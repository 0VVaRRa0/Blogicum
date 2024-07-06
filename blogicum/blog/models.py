from django.db import models
from django.utils import timezone
from django.utils.text import Truncator

from .constants import (
    MAX_TITLE_LENGTH, TITLE_DISPLAY_LIMIT, USER
)
from core.models import PublishableTimestampedModel


class Category(PublishableTimestampedModel):
    title = models.CharField(
        max_length=MAX_TITLE_LENGTH,
        verbose_name='Заголовок'
    )
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=('Идентификатор страницы для URL; '
                   'разрешены символы латиницы, цифры, '
                   'дефис и подчёркивание.')
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return Truncator(self.title).chars(TITLE_DISPLAY_LIMIT)


class Location(PublishableTimestampedModel):
    name = models.CharField(
        max_length=MAX_TITLE_LENGTH,
        verbose_name='Название места'
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return Truncator(self.name).chars(TITLE_DISPLAY_LIMIT)


class Post(PublishableTimestampedModel):
    title = models.CharField(
        max_length=MAX_TITLE_LENGTH,
        verbose_name='Заголовок'
    )
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата и время публикации',
        help_text=('Если установить дату и время в будущем '
                   '— можно делать отложенные публикации.')
    )
    author = models.ForeignKey(
        USER,
        verbose_name='Автор публикации',
        related_name='posts',
        on_delete=models.CASCADE
    )
    location = models.ForeignKey(
        Location,
        verbose_name='Местоположение',
        related_name='posts',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        related_name='posts',
        on_delete=models.SET_NULL,
        null=True
    )
    image = models.ImageField(
        'Изображение',
        upload_to='blog_images',
        blank=True
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return Truncator(self.title).chars(TITLE_DISPLAY_LIMIT)


class Comment(models.Model):
    author = models.ForeignKey(
        USER,
        verbose_name='Автор',
        related_name='comments',
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post,
        verbose_name='Пост',
        related_name='comments',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField('Текст комментария')

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return Truncator(self.text).chars(TITLE_DISPLAY_LIMIT)
