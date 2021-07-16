from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler

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
        fields = ['post_id', 'date', 'time']
        read_only_fields = ['date', 'time']

    def create(self, validated_data):
        try:
            return Like.objects.create(**validated_data)
        except IntegrityError:
            # Raise an error because post and user aren't unique together
            raise ValidationError("You already like this post")

    def validate(self, validated_data):
        """
        Validate post field using post_id
        if post doesn't exist, raise ValidationError
        else add post fiedl in validated_data
        """
        post_id = validated_data['post_id']
        post = get_object_or_none(Post, pk=post_id)
        if post is None:
            raise ValidationError("Post with that post_id doesn't exist")

        del validated_data['post_id']
        validated_data['post'] = post
        return validated_data

    def delete(self, validated_data):
        print(validated_data)
        pass


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # if response.data is list change it to dict
    if isinstance(response.data, list):
        response.data = {'error': response.data}
    return response


class UnlikeSerializer(serializers.ModelSerializer):
    """ Serializer for create Like """
    post_id = serializers.IntegerField(min_value=1, write_only=True)

    class Meta:
        model = Like
        fields = ['post_id', 'date', 'time']
        read_only_fields = ['date', 'time']
