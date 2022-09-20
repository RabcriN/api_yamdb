from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TitleViewSet, GenreViewSet, CategoryViewSet
# from users.views import UserViewSet  # надо думать

router = DefaultRouter()
router.register('titles', TitleViewSet)
router.register('genres', GenreViewSet)
router.register('categories', CategoryViewSet)
# router.register('users', UserViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]
