from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
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
    post_id = serializers.IntegerField(min_value=1, write_only=True)

    class Meta:
        model = Like
        # fields = ['id', 'post_id', 'date', 'time']
        # read_only_fields = ['date', 'time']
        fields = ['id', 'post_id', 'create_at']
        read_only_fields = ['create_at']

    def create(self, validated_data):
        try:
            return Like.objects.create(**validated_data)
        except IntegrityError:
            # Raise an error because post and user aren't unique together
            raise ValidationError("You already like this post")

    def validate(self, validated_data):
        """
        Validate post_id field
        if post doesn't exist, raise ValidationError
        else add post in validated_data
        """
        post_id = validated_data['post_id']
        post = get_object_or_none(Post, pk=post_id)
        if post is None:
            raise ValidationError("Post with that post_id doesn't exist")

        del validated_data['post_id']
        validated_data['post'] = post
        return validated_data


class UnlikeSerializer(serializers.ModelSerializer):
    """ Serializer for create Like """
    post_id = serializers.IntegerField(min_value=1, write_only=True)

    class Meta:
        model = Like
        fields = ['post_id', ]

    def save(self, user):
        post = self.validated_data.get('post')
        like = get_object_or_none(Like, post=post, user=user)
        if not like:
            raise ValidationError("You can't delete this like.")
        like.delete()

    def validate(self, validated_data):
        """
        Validate like_id field
        if like doesn't exist raise ValidationError
        else add like in validation_data
        """
        post_id = validated_data['post_id']
        post = get_object_or_none(Post, pk=post_id)
        if post is None:
            raise ValidationError("Post with that post_id doesn't exist")

        validated_data['post'] = post
        return validated_data


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
