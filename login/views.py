from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .serializers import LoginSerializer, TokenSerializer, UserSerializer


class TokenView(APIView):

    serializer_class = LoginSerializer

    def post(self, request: Request) -> Response:
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username_password = serializer.validated_data
        user = User.objects.filter(
            username=username_password['username']).first()
        if user and user.check_password(username_password['password']):
            Token.objects.filter(user=user).delete()
            token = Token.objects.create(user=user)
            return Response(
                TokenSerializer(token).data, status=status.HTTP_200_OK
            )

        return Response(status=status.HTTP_401_UNAUTHORIZED)


class UserView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request: Request) -> Response:
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
