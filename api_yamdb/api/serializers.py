from django.shortcuts import get_object_or_404
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
        # Если дальше поменять на '__all__', то валятся тесты, т.к. не хватает
        # поля id. К тому же явное лучше неявного.
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
        read_only=True,
        slug_field='username')
    title = serializers.SlugRelatedField(
        read_only=True, slug_field='name')

    def validate(self, data):
        request = self.context['request']
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(
                title=title, author=request.user
            ).exists():
                raise ValidationError('Only one review is allowed')
        return data

    class Meta:
        fields = ("id", "text", "author", "score", "pub_date", 'title')
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
