from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views import UserViewSet, UserInfoViewSet

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

router.register('users/me', UserInfoViewSet, basename='userinfo')
router.register('users', UserViewSet, basename='username')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/', include('djoser.urls.authtoken')),
    path('v1/auth/', include('djoser.urls.jwt')),
    # path('v1/auth/signup/', SignUpViewSet.as_view(), name='signup')
]
