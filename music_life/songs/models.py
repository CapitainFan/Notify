from django.db import models
from django.urls import reverse

class Songs(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="Заголовок",
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
        verbose_name="URL",
    )
    content = models.TextField(
        blank=True,
        verbose_name="Текст статьи",
    )
    photo = models.ImageField(
        upload_to="photos/%Y/%m/%d/",
        verbose_name="Фото",
    )
    time_create = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время создания",
    )
    time_update = models.DateTimeField(
        auto_now=True,
        verbose_name="Время изменения",
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name="Публикация",
    )
    genre = models.ForeignKey(
        'Genre', 
        on_delete=models.PROTECT,
        verbose_name="Жанр",
    )
    author = models.ForeignKey(
        'Author',
        on_delete=models.PROTECT,
        verbose_name="Исполнитель",
    )
    album = models.ForeignKey(
        'Album',
        on_delete=models.PROTECT,
        verbose_name='Альбом',
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('song', kwargs={'song_slug': self.slug})

    class Meta:
        verbose_name = 'Песни'
        verbose_name_plural = 'Песня'
        ordering = ['id']


class Genre(models.Model):
    name = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name="Жанр",
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
        verbose_name="URL",
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('genre', kwargs={'genre_slug': self.slug})

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['id']


class Author(models.Model):
    name = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name="Автор",
    )
    content = models.TextField(
        blank=True,
        verbose_name="Про исполнителя",
    )
    photo = models.ImageField(
        upload_to="photos/%Y/%m/%d/",
        verbose_name="Фото",
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
        verbose_name="URL",
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('author', kwargs={'author_slug': self.slug})

    class Meta:
        verbose_name = 'Исполнитель'
        verbose_name_plural = 'Исполнители'
        ordering = ['id']


class Album(models.Model):
    name = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name="Альбом",
    )
    author = models.ForeignKey(
        'Author',
        verbose_name='Исполнитель'
    )
    photo = models.ImageField(
        upload_to="photos/%Y/%m/%d/",
        verbose_name="Фото",
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
        verbose_name="URL",
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('album', kwargs={'album_slug': self.slug})

    class Meta:
        verbose_name = 'Альбом'
        verbose_name_plural = 'Альбомы'
        ordering = ['id']
