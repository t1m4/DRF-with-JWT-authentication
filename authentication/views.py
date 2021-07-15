# Create your views here.
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from authentication.serializers import RegistrationSerializer
from authentication.tools import get_tokens_for_user


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


class RegistrationAPIView(APIView):
    """
    Register point for users
    """
    permission_classes = (AllowAny,)
    throttle_classes = [UserRateThrottle]
    serializer_class = RegistrationSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.POST)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            token.update(serializer.data)
            return Response(token, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
