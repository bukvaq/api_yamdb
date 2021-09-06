from django.shortcuts import render

from rest_framework import viewsets

from users.models import User
from reviews.models import *


class UserViewSet(viewsets.ModelViewSet):
    pass


class TitlesViewSet(viewsets.ModelViewSet):
    pass


class CategoriesViewSet(viewsets.ModelViewSet):
    pass


class GenresViewSet(viewsets.ModelViewSet):
    pass


class ReviewsViewSet(viewsets.ModelViewSet):
    pass


class CommentsViewSet(viewsets.ModelViewSet):
    pass

