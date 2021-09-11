from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from api.validator import year_validator
from users.models import User


class Category(models.Model):
    """Модель для хранения категорий."""
    name = models.CharField(max_length=256, verbose_name='Category name')
    slug = models.SlugField(
        max_length=50, unique=True, verbose_name='Category slug'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Genre(models.Model):
    """Модель для хранения жанров."""
    name = models.CharField(max_length=256, verbose_name='Genre name')
    slug = models.SlugField(
        max_length=50, unique=True, verbose_name='Genre slug'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'


class Title(models.Model):
    """Модель для хранения названий произведений."""
    name = models.CharField(max_length=256, verbose_name='Artwork title')
    year = models.IntegerField(
        validators=[year_validator], verbose_name='Artwork year'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='titles', blank=True, null=True,
        verbose_name='Artwork category'
    )
    genre = models.ManyToManyField(Genre, verbose_name='Artwork genre')
    description = models.TextField(
        blank=True, verbose_name='Artwork description'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Title'
        verbose_name_plural = 'Titles'


class Review(models.Model):
    """Модель для хранения обзоров,
    оценки можно ставить от 1 до 10."""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews', null=True
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        auto_now_add=True, db_index=True
    )
    score = models.IntegerField(default=1, validators=[
        MaxValueValidator(10, 'Оценка не может быть больше 10'),
        MinValueValidator(1, 'Оценка не может быть меньше 1')
    ])

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name='unique_reviews'
            ),
        ]
        ordering = ['-pub_date']
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель для комментариев под обзорами."""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return self.text
