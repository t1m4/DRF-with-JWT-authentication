# Create your views here.

from django.db.models import Q, Count, DateField
from django.db.models.functions import TruncDay, Cast
from django.utils.timezone import make_aware
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from social_network.models import Like
from social_network.serializers import CreatePostSerializer, CreateLikeSerializer, UnlikeSerializer, DateSerializer
from social_network.tools import from_date_to_datetime


class CreatePostAPIView(APIView):
    serializer_class = CreatePostSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.POST)
        serializer.is_valid(raise_exception=True)
        # pass a user
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LikeAPIView(APIView):
    serializer_class = CreateLikeSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.POST)
        serializer.is_valid(raise_exception=True)
        # pass a user
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UnlikeAPIView(APIView):
    serializer_class = UnlikeSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.POST)
        serializer.is_valid(raise_exception=True)
        # pass a user
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class AnalyticsAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DateSerializer

    def get(self, request):
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        data = {
            'date_from': date_from,
            'date_to': date_to
        }
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        result = self.get_user_likes(request, serializer.validated_data)
        return Response(result, status.HTTP_200_OK)

    def get_user_likes(self, request, data, *args, **kwargs):
        """
        Getting likes from user posts, group by day and count
        """
        date_from = make_aware(from_date_to_datetime(data.get('date_from')))
        date_to = make_aware(from_date_to_datetime(data.get('date_to')))

        result = Like.objects.filter(
            Q(create_at__gte=date_from) &
            Q(create_at__lte=date_to) &
            # Q(user=request.user) # like made by user
            Q(post__user=request.user)  # like made for user's post
        ).annotate(
            day=TruncDay('create_at', output_field=DateField())
        ).values('day').annotate(count=Count('id'))
        return result


class ActivityAPIView(APIView):
    pass
