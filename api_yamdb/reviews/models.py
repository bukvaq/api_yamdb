from django.contrib.auth import get_user_model
from django.db import models


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
    genre = models.ForeignKey(Genres, on_delete=models.PROTECT)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
