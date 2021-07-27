from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.views import exception_handler

from authentication.models import User
from social_network.models import Post, Like
from social_network.tools import get_object_or_none


class CreatePostSerializer(serializers.ModelSerializer):
    """ Serializer for create Post """

    class Meta:
        model = Post
        fields = ['id', 'title', 'description']
        read_only_fields = ['id', ]


class CreateLikeSerializer(serializers.ModelSerializer):
    """ Serializer for create Like """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Like
        fields = ['id', 'post', 'user', 'create_at']
        read_only_fields = ['create_at']
        validators = [
            UniqueTogetherValidator(
                queryset=Like.objects.all(),
                fields=['user', 'post']
            )
        ]


class UnlikeSerializer(serializers.ModelSerializer):
    """ Serializer for create Like """

    class Meta:
        model = Like
        fields = ['post', ]

    def save(self, *args, **kwargs):
        post = self.validated_data.get('post')
        user = kwargs.pop('user')
        like = get_object_or_none(Like, post=post, user=user)
        if like:
            like.delete()
        else:
            raise serializers.ValidationError("Like doesn't exist'")


class DateSerializer(serializers.Serializer):
    """ Serializer for validate date """
    date_from = serializers.DateField()
    date_to = serializers.DateField()

    def validate(self, validated_data):
        """
        Date_to must occur after date_from
        """
        if validated_data['date_from'] > validated_data['date_to']:
            raise serializers.ValidationError("date_to must occur after date_from")
        return validated_data


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)

    def validate(self, validated_data):
        """
        user must exist
        """
        username = validated_data['username']
        user = get_object_or_none(User, username=username)
        if user is None:
            raise ValidationError("User doesn't exist")
        else:
            validated_data['user'] = user
        return validated_data


def custom_exception_handler(exc, context):
    # get the standard error response.
    response = exception_handler(exc, context)

    # if response.data is list change it to dict
    if response is not None:
        if isinstance(response.data, list):
            response.data = {'error': response.data}
    return response
