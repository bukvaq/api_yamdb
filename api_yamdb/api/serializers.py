from rest_framework import serializers
from rest_framework.validators import UniqueValidator

import datetime as dt

from users.models import User
from reviews.models import Comments, Reviews, Categories, Genres, Titles


class EmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ('email', 'username')


class ConfirmationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class UserForAdminSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'role', 'bio')


class UserSerializer(UserForAdminSerializer):
    role = serializers.CharField(read_only=True)


class CategoriesSerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    class Meta:
        fields = ('name', 'slug')
        model = Categories


class GenresSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""

    class Meta:
        fields = ('name', 'slug')
        model = Genres


class TitlesSerializer(serializers.ModelSerializer):
    """Сериализатор для названий произведений."""
    genre = GenresSerializer(many=True, read_only=True)
    category = CategoriesSerializer(read_only=True)
    score = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Titles

    def validate_title_year(self, value):
        year = dt.date.today().year
        if not (value <= year):
            raise serializers.ValidationError('Проверьте год произведения!')
        return value


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев,
    дату, автора и все id можно только получить."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comments
        fields = ('id', 'review_id', 'text', 'pub_date', 'author')
        read_only_fields = ('id', 'pub_date', 'author', 'review_id')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для обзоров,
    дату, автора и все id можно только получить."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        if Reviews.objects.filter(
            author=data['author'], title_id=data['title_id']
        ).exists():
            raise serializers.ValidationError(
                'Нельзя создавать больше одного обзора'
            )
        return data

    class Meta:
        model = Reviews
        fields = ('id', 'title_id', 'text', 'pub_date', 'author', 'score')
        read_only_fields = ('id', 'pub_date', 'author', 'title_id')
