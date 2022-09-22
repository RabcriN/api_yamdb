from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (TitleViewSet, GenreViewSet, CategoryViewSet,
                    CommentViewSet, ReviewViewSet)


router = DefaultRouter()
router.register('titles', TitleViewSet)
router.register('genres', GenreViewSet)
router.register('categories', CategoryViewSet)
router.register(
    r'titles/(?P<title_id>[^/.]+)/reviews',
    ReviewViewSet,
    basename='reviews')
router.register(
    r'titles/(?P<title_id>[^/.]+)/reviews/(?P<review_id>[^/.]+)/comments',
    CommentViewSet,
    basename='comments')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/auth/', include('djoser.urls.authtoken')),
    path('v1/auth/', include('djoser.urls.jwt')),
]
