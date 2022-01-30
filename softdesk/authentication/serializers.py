from rest_framework import serializers
from authentication.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for create account endpoint.
    """
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'password']

    def create(self, validated_data):
        user = super(CustomUserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class ChangePasswordCustomUserSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    class Meta:
        model = CustomUser

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
