from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters, mixins
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Categories, Title, Genres, Review
from users.models import User
from .filters import CustomFilter
from .permissions import IsAdmin, ReviewPermission, AdminPermissionOrReadOnly
from .serializers import (
    UserSerializer,
    ConfirmationSerializer,
    EmailSerializer,
    UserForAdminSerializer,
    CommentSerializer,
    ReviewSerializer,
    GenresSerializer,
    CategoriesSerializer,
    TitlesSerializer,
    TitleSerializerCreateUpdate
)


@api_view(['POST'])
def signup(request):
    """функция для авторизации, получение кода проверки на почту"""
    serializer_data = EmailSerializer(data=request.data)
    serializer_data.is_valid(raise_exception=True)
    email = serializer_data.data.get('email')
    username = serializer_data.data.get('username')
    if username == 'me':
        return Response('неверное имя пользователя',
                        status=status.HTTP_400_BAD_REQUEST)
    user, create = User.objects.get_or_create(email=email, username=username)
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Отправляем код для проверки электронной почты',
        f'Ваш код подтверждения: {confirmation_code}',
        settings.DEFAULT_FROM_EMAIL, [email])
    return Response({'email': email, 'username': username})


@api_view(['POST'])
def get_token(request):
    """функция для получения токена после введения кода проверки из почты"""
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
    """Вьюсет для Пользователей"""
    queryset = User.objects.all()
    serializer_class = UserForAdminSerializer
    permission_classes = [IsAdmin]
    lookup_field = "username"
    filter_backends = [filters.SearchFilter]
    search_fields = ["=username", ]

    @action(
        detail=False,
        methods=["get", "patch"],
        permission_classes=[IsAuthenticated, ])
    def me(self, request):
        user = get_object_or_404(User, pk=request.user.id)
        if request.method == 'GET':
            serializer = UserSerializer(user, many=False)
            return Response(serializer.data)
        if request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class CustomViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                    mixins.ListModelMixin, viewsets.GenericViewSet):
    """Кастомный вьюсет для Категорий и для Жанров"""
    pass


class CategoriesViewSet(CustomViewSet):
    """Вьюсет для категорий."""
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = "slug"
    permission_classes = (AdminPermissionOrReadOnly,)


class TitlesViewSet(viewsets.ModelViewSet):
    """Вьюсет для названий произведений."""
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    filterset_fields = ('category', 'genre', 'name', 'year')
    permission_classes = (AdminPermissionOrReadOnly,)
    filterset_class = CustomFilter

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update', 'destroy']:
            return TitleSerializerCreateUpdate
        return TitlesSerializer


class GenresViewSet(CustomViewSet):
    """Вьюсет для жанров."""
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (AdminPermissionOrReadOnly,)


class ReviewsViewSet(viewsets.ModelViewSet):
    """Вьюсет для обзоров."""
    permission_classes = (ReviewPermission,)
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(ReviewsViewSet):
    """Вьюсет для комментариев,
    наследуется от вьюсета обзоров"""
    serializer_class = CommentSerializer

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        serializer.save(author=self.request.user, review=review)
