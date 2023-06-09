from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class Author(models.Model):
    '''
    Модель исполнителя песен
    '''
    name = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name='Имя исполнителя',
        unique=True,
    )
    content = models.TextField(
        max_length=50000,
        blank=True,
        verbose_name='Про исполнителя',
    )
    photo = models.ImageField(
        upload_to='photos/%Y/%m/%d/',
        verbose_name='Фото',
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
        verbose_name='URL',
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('author', kwargs={'author_slug': self.slug})

    class Meta:
        verbose_name = 'Исполнитель'
        verbose_name_plural = 'Исполнители'
        ordering = ['name']


class Album(models.Model):
    '''
    Модель альбомов
    '''
    name = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name='Название альбома',
    )
    author = models.ForeignKey(
        Author,
        verbose_name='Исполнитель',
        related_name='get_album',
        on_delete=models.PROTECT,
    )
    photo = models.ImageField(
        upload_to='photos/%Y/%m/%d/',
        verbose_name='Фото',
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
        verbose_name='URL',
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('album', kwargs={'album_slug': self.slug})

    class Meta:
        verbose_name = 'Альбом'
        verbose_name_plural = 'Альбомы'
        ordering = ['name']


class Genre(models.Model):
    '''
    Модель жанров песен
    '''
    name = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name='Навание жанра',
        unique=True,
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
        verbose_name='URL',
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('genre', kwargs={'genre_slug': self.slug})

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']


class Songs(models.Model):
    '''
    Модель песен
    '''
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='post',
        verbose_name='Пользователь')
    title = models.CharField(
        max_length=255,
        verbose_name='Название песни',
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
        verbose_name='URL',
    )
    content = models.TextField(
        max_length=50000,
        verbose_name='Информация',
    )
    photo = models.ImageField(
        upload_to='photos/%Y/%m/%d/',
        verbose_name='Фото',
    )
    time_create = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создания',
    )
    time_update = models.DateTimeField(
        auto_now=True,
        verbose_name='Время изменения',
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name='Публикация',
    )
    is_single = models.BooleanField(
        default=True,
        verbose_name='Сингл',
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанры',
        related_name='get_songs',
    )
    author = models.ManyToManyField(
        Author,
        verbose_name='Исполнители',
        related_name='get_songs',
    )
    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        verbose_name='Альбом',
        related_name='get_songs',
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    def clean_email(self):
        if self.is_single and self.album is not None:
            raise ValidationError(
                "Песня не может быть одновременно синглом и входить в альбом"
            )
        if not self.is_single and self.album is None:
            raise ValidationError(
                "Песня не может быть не синглом и не входить в альбом"
            )

    class Meta:
        verbose_name = 'Песня'
        verbose_name_plural = 'Песни'
        ordering = ['title']
