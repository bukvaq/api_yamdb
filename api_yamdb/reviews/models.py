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
