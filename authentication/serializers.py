from django.contrib.auth import password_validation
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from authentication.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    """ Serialisation for register """

    # Minimum 8 lenght, and couldn't see by client side
    password = serializers.CharField(max_length=128, min_length=8, write_only=True, style={'input_type': 'password'})
    double_password = serializers.CharField(max_length=128, min_length=8, write_only=True,
                                            style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'double_password']

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate(self, data):
        """
        Validate and Check that passwords are equal
        """
        # Validate password
        password_validation.validate_password(data['password'])

        # Check password
        if data['password'] != data['double_password']:
            raise ValidationError('Passwords are not equal')
        return data
