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


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(required=False)
    category = CategorySerializer()

    class Meta:
        fields = '__all__'
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field="slug",
        queryset=Genre.objects.all()
    )
    rating = serializers.IntegerField(required=False)
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all()
    )

    def to_representation(self, instance):
        serializer = TitleReadSerializer(instance)
        return serializer.data

    class Meta:
        fields = '__all__'
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
        slug_field="username")
    title = serializers.SlugRelatedField(
        read_only=True, slug_field="name")

    def validate(self, data):
        request = self.context["request"]
        title_id = self.context['view'].kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        if request.method == "POST" and Review.objects.filter(
            title=title,
            author=request.user
        ).exists():
            raise ValidationError("?????????? ???????????????? ???????????? ???????? ??????????!")
        return data

    class Meta:
        fields = ("id", "text", "author", "score", "pub_date", 'title')
        model = Review


class UserSerializer(serializers.ModelSerializer):
    """???????????????????????? ?????????????????????????? ???? ???????????????? ??????????."""

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
    """???????????????????????? ?????????????????????? ????????????????????????."""

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
            raise ValidationError('username ???? ?????????? ???????? "me"')
        return value


class TokenSerializer(serializers.Serializer):
    """???????????????????????? ?????????????????? ????????????."""
    username = serializers.CharField()
    confirmation_code = serializers.CharField()
