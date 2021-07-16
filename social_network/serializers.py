from rest_framework import serializers

from social_network.models import Post


class CreatePostSerializer(serializers.ModelSerializer):
    """ Serialiser for create post """

    class Meta:
        model = Post
        fields = ['id', 'title', 'description']
        read_only_fields = ['id', ]
