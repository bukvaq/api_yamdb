from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import User
from reviews.models import Comment, Review


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


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев,
    дату, автора и все id можно только получить."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'review_id', 'text', 'pub_date', 'author')
        read_only_fields = ('id', 'pub_date', 'author', 'review_id')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для обзоров,
    дату, автора и все id можно только получить."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'title_id', 'text', 'pub_date', 'author', 'score')
        read_only_fields = ('id', 'pub_date', 'author', 'title_id')
