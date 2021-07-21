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
        del validated_data['double_password']
        return User.objects.create(**validated_data)

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
