from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, ValidationError
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "name",
            "slug",
        )
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "name",
            "slug",
        )
        model = Genre


class CategoryField(serializers.Field):
    def to_representation(self, value):
        return CategorySerializer(value).data

    def to_internal_value(self, data):
        return Category.objects.get(slug=data)


class GenreField(serializers.RelatedField):
    def get_queryset(self):
        return Genre.objects.all()

    def to_representation(self, value):
        return GenreSerializer(value).data

    def to_internal_value(self, data):
        return Genre.objects.get(slug=data)


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreField(many=True)
    rating = serializers.IntegerField(required=False)
    category = CategoryField()

    class Meta:
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )
        model = Title


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    class Meta:
        fields = ("id", "text", "author", "pub_date")
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    def validate(self, data):
        print("validate", data)
        return data

    class Meta:
        fields = ("id", "text", "author", "score", "pub_date")
        model = Review


class UserSerializer(serializers.ModelSerializer):
    """Сериализация пользователей со статусом юзера."""

    class Meta:
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        model = User
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(), fields=["username", "email"]
            )
        ]


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализация регистрации пользователя."""

    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(), fields=["username", "email"]
            )
        ]

    def validate_username(self, value):
        if value.lower() == "me":
            raise ValidationError('username не может быть "me"')
        return value


class TokenSerializer(serializers.Serializer):
    """Сериализация получения токена."""

    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = ["username", "confirmation_code"]
        ordering = ["username"]
