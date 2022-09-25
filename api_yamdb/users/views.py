from api.permissions import IsAdminOnly
from api.serializers import SignUpSerializer, TokenSerializer, UserSerializer
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenViewBase
from users.models import User


def send_confirmation_code(user):
    """Отправка кода на почту"""
    confirmation_code = default_token_generator.make_token(user)
    subject = "Код подтверждения на сервисе YaMDb"
    message = f"{confirmation_code} - ваш код авторизации на сервисе YaMDb"
    admin_email = settings.DEFAULT_FROM_EMAIL
    user_email = [user.email]
    return send_mail(subject, message, admin_email, user_email)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (
        IsAuthenticated,
        IsAdminOnly,
    )
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ("username",)
    lookup_field = "username"

    @action(
        detail=False,
        methods=("GET", "PATCH"),
        url_path="me",
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        """Профайл пользователя."""
        if request.method == "GET":
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        # а если PATCH-запрос:
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


class APISignup(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        """Создание и отправка."""
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_confirmation_code(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIGetToken(TokenViewBase):
    """Получение JWT-токена."""

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        username = serializer.data["username"]
        user = get_object_or_404(User, username=username)
        confirmation_code = serializer.data["confirmation_code"]
        if not default_token_generator.check_token(user, confirmation_code):
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        token = AccessToken.for_user(user)
        return Response({"token": str(token)}, status=status.HTTP_200_OK)
