from django.utils import timezone
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Comment, Review, Category, Genre, Title
from users.models import User


class EmailSerializer(serializers.ModelSerializer):
    """Сериализатор для электронной почты и ник-нейма."""
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Некорректный ник-нейм!')
        return value


class ConfirmationSerializer(serializers.ModelSerializer):
    """Сериализатор для кода подтверждения."""
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class UserForAdminSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей."""
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'role', 'bio')


class UserSerializer(UserForAdminSerializer):
    """Сериализатор для пользователя-админа."""
    role = serializers.CharField(read_only=True)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    class Meta:
        exclude = ('id',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""

    class Meta:
        exclude = ('id',)
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для названий произведений, метод 'list' """
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title

    def validate_title_year(self, value):
        year = timezone.now().year
        if not (value <= year):
            raise serializers.ValidationError('Проверьте год произведения!')
        return value


class TitleSerializerCreateUpdate(serializers.ModelSerializer):
    """Сериализатор для названий произведений, методы
    'create', 'partial_update', 'destroy' """
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all(), required=False)
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True,
        required=False)

    class Meta:
        model = Title
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев,
    дату, автора и все id можно только получить."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'review', 'text', 'pub_date', 'author')
        read_only_fields = ('id', 'pub_date', 'author', 'review')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для обзоров,
    дату, автора и все id можно только получить."""
    title = serializers.SlugRelatedField(
        slug_field='name', read_only=True)
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault())

    def validate(self, data):
        request = self.context.get('request')
        if request.method != 'POST':
            return data
        title = self.context.get('view').kwargs.get('title_id')
        if Review.objects.filter(author=request.user, title=title).exists():
            raise serializers.ValidationError(
                'Нельзя создавать больше одного обзора'
            )
        return data

    class Meta:
        model = Review
        fields = ('id', 'title', 'text', 'pub_date', 'author', 'score')
        read_only_fields = ('id', 'pub_date', 'author', 'title')
