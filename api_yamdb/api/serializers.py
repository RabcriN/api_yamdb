from titles.models import Title, Genre, Category, Review, Comment
from users.models import User
from rest_framework import serializers


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.ReadOnlyField(source='category.name')
    genre = serializers.ReadOnlyField(source='genre.name')

    class Meta:
        fields = (
            'name',
            'year',
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


class SignUpSerializer(serializers.ModelSerializer):
    pass


class UserSerializer(serializers.ModelSerializer):

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
