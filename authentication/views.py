# Create your views here.
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from authentication.serializers import RegistrationSerializer


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


class ThrottleTokenObtainPairView(TokenObtainPairView):
    """
    Throttle Login point for users
    """
    throttle_classes = [AnonRateThrottle]


# class RegistrationAPIView(generics.GenericAPIView):
class RegistrationAPIView(APIView):
    """
    Register point for users
    """
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.POST)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # generate tokens and add them to the result
        data = user.tokens
        data.update(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED)
