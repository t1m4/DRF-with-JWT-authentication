# Create your views here.
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from social_network.serializers import CreatePostSerializer


class CreatePostAPIView(APIView):
    serializer_class = CreatePostSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.POST)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LikeAPIView(APIView):
    pass


class UnlikeAPIView(APIView):
    pass


class AnaliticsAPIView(APIView):
    pass


class ActivityAPIView(APIView):
    pass
