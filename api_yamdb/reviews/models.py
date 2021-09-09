from django.db import models

from users.models import User


class Categories(models.Model):
    """Модель для хранения категорий."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genres(models.Model):
    """Модель для хранения жанров."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель для хранения названий произведений."""
    name = models.CharField(max_length=256)
    year = models.IntegerField()

    category = models.ForeignKey(
        Categories, on_delete=models.SET_NULL,
        related_name='titles', blank=True, null=True
    )
    genre = models.ManyToManyField(Genres)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель для хранения обзоров,
    оценки можно ставить от 1 до 10."""

    SCORE_CHOICES = [(i, str(i)) for i in range(1, 11)]

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
    score = models.IntegerField(choices=SCORE_CHOICES)

    def __str__(self):
        return self.text

    class Meta:
        unique_together = ('author', 'title')


class Comments(models.Model):
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

    def __str__(self):
        return self.text
