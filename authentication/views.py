# Create your views here.
import logging

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenViewBase

from authentication.serializers import RegistrationSerializer

logger = logging.getLogger('starnavi.console_logger')


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


class LoginAPIView(TokenViewBase):
    """
    Register point for users
    """
    serializer_class = TokenObtainPairSerializer
    throttle_classes = [AnonRateThrottle]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        serializer.user.update_last_login()
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class RegistrationAPIView(APIView):
    """
    Register point for users
    """
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.POST)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # generate tokens and add them to the result
        data = user.tokens
        data.update(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED)
