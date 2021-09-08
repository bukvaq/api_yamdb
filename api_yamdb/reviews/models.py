from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from users.models import User


class Categories(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    category = models.ForeignKey(Categories, on_delete=models.PROTECT)
    genre = models.ManyToManyField(Genres, on_delete=models.PROTECT)
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
    title_id = models.ForeignKey(
        Titles, on_delete=models.CASCADE, related_name='reviews'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        auto_now_add=True, db_index=True
    )
    score = models.IntegerField(choices=SCORE_CHOICES)

    def __str__(self):
        return self.text

    class Meta:
        unique_together = ('author', 'title_id')


class Comment(models.Model):
    """Модель для комментариев под обзорами."""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    review_id = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        auto_now_add=True, db_index=True
    )

    def __str__(self):
        return self.text
