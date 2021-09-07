from reviews.models import Categories, Titles, Genres
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.pagination import PageNumberPagination

from users.models import User
from .permissions import IsAdmin, AdminPermissionOrReadOnly
from .serializers import (
    UserSerializer,
    ConfirmationSerializer,
    EmailSerializer,
    UserForAdminSerializer,
    GenresSerializer,
    CategoriesSerializer,
    TitlesSerializer)


@api_view(['POST'])
def signup(request):
    serializer_data = EmailSerializer(data=request.data)
    serializer_data.is_valid(raise_exception=True)
    email = serializer_data.data.get('email')
    username = serializer_data.data.get('username')
    if username == '':
        return Response('неверное имя пользователя',
                        status=status.HTTP_400_BAD_REQUEST)
    if username == 'me':
        return Response('неверное имя пользователя',
                        status=status.HTTP_400_BAD_REQUEST)
    user, create = User.objects.get_or_create(email=email, username=username,
                                              )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Отправляем код для проверки электронной почты',
        f'Ваш код подтверждения: {confirmation_code}',
        settings.DEFAULT_FROM_EMAIL, [email])
    return Response({'email': email, 'username': username})


@api_view(['POST'])
def get_token(request):
    serializer_data = ConfirmationSerializer(data=request.data)
    serializer_data.is_valid(raise_exception=True)
    confirmation_code = serializer_data.data.get('confirmation_code')
    username = serializer_data.data.get('username')
    user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(user, confirmation_code):
        user.is_active = True
        user.save()
        token = AccessToken.for_user(user)
        return Response({'token': f'{token}'}, status=status.HTTP_200_OK)
    return Response('Неверный код подтверждения',
                    status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    pass


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter)
    search_fields = ('name',)
    permission_classes = (AdminPermissionOrReadOnly,)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend)
    filterset_fields = ('category', 'genre', 'name', 'year')
    permission_classes = (AdminPermissionOrReadOnly,)


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter)
    search_fields = ('name',)
    permission_classes = (AdminPermissionOrReadOnly,)


class ReviewsViewSet(viewsets.ModelViewSet):
    pass


class CommentsViewSet(viewsets.ModelViewSet):
    pass
