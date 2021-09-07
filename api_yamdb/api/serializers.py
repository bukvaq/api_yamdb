from rest_framework import serializers
from rest_framework.validators import UniqueValidator

import datetime as dt

from users.models import User
from reviews.models import Categories, Genres, Titles


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
    slug = serializers.SlugField(validators=[UniqueValidator(
        queryset=Categories.objects.all())])

    class Meta:
        fields = '__all__'
        model = Categories


class GenresSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(validators=[UniqueValidator(
        queryset=Categories.objects.all())])

    class Meta:
        fields = '__all__'
        model = Genres


class TitlesSerializer(serializers.ModelSerializer):
    genre = serializers.StringRelatedField(many=True)

    class Meta:
        fields = '__all__'
        model = Titles

    def validate_title_year(self, value):
        year = dt.date.today().year
        if not (value <= year):
            raise serializers.ValidationError('Проверьте год произведения!')
        return value
