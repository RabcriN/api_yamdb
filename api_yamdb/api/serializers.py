from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, ValidationError
from titles.models import Category, Comment, Genre, Review, Title
from users.models import User


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.ReadOnlyField(source='category.name')
    genre = serializers.ReadOnlyField(source='genre.name')
    rating = serializers.IntegerField()

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )
        model = Title


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug',)
        model = Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug',)
        model = Category


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username')

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review


class UserSerializer(serializers.ModelSerializer):
    """Сериализация пользователей со статусом юзера."""
    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        model = User
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            )
        ]


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализация регистрации пользователя."""
    class Meta:
        model = User
        fields = ('username', 'email',)
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            )
        ]

    def validate_username(self, value):
        if value.lower() == 'me':
            raise ValidationError('username не может быть "me"')
        return value


class TokenSerializer(serializers.Serializer):
    """Сериализация получения токена."""
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = ['username', 'confirmation_code']
        ordering = ['username']
