from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from .permissions import (IsAdminOrReadOnly, IsAdminOnly,
                          IsAuthorModeratorAdmin)
from titles.models import Category, Genre, Title, Review
from users.models import User
from .serializers import (TitleSerializer, GenreSerializer, CategorySerializer,
                          ReviewSerializer, CommentSerializer,
                          SignUpSerializer, UserSerializer)
from django_filters.rest_framework import DjangoFilterBackend


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filterset_fields = ('category', 'genre', 'name', 'year',)
    http_method_names = ('get', 'post', 'patch', 'delete',)
    pagination_class = PageNumberPagination


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    http_method_names = ('get', 'post', 'delete',)
    pagination_class = PageNumberPagination


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    http_method_names = ('get', 'post', 'delete',)
    pagination_class = PageNumberPagination


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorModeratorAdmin,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorModeratorAdmin,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review, id=title.id)


class SignUpViewSet(viewsets.ModelViewSet):
    serializer_class = SignUpSerializer
    # это пока просто заглушка для /auth/


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    lookup_field = "username"
    http_method_names = ('get', 'post', 'patch', 'delete',)
    serializer_class = UserSerializer
    permission_classes = (IsAdminOnly,)


class UserInfoViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    http_method_names = ('get', 'patch',)
    serializer_class = UserSerializer
    permission_classes = (IsAdminOnly,)

    def get_queryset(self):
        return self.queryset.filter(username=self.request.user.username)
