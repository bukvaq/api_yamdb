from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, action
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from rest_framework import viewsets, status
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from users.models import User
from reviews.models import *
from .serializers import *


@api_view(['POST'])
def signup(request):
    serializer_data = EmailSerializer(data=request.data)
    serializer_data.is_valid(raise_exception=True)
    email = serializer_data.data.get('email')
    username = serializer_data.data.get('username')
    if username == 'me':
        return Response('неверное имя пользователя',
                        status=status.HTTP_400_BAD_REQUEST)
    user, create = User.objects.get_or_create(email=email, username=username,
                                              is_active=False)
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
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(
        detail=False,
        methods=["get", "patch"],
        permission_classes=[IsAuthenticated],)
    def me(self, request):
        user = get_object_or_404(User, pk=request.user.id)
        if request.metod == 'GET':
            serializer = UserSerializer(user, many=False)
            return Response(serializer.data)
        if request.metod == 'PATCH':
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)



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

