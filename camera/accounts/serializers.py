from rest_framework import serializers
from .models import User, Profile


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User
    """
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for Login View
    """
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class ChangePasswordSerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password_1 = serializers.CharField(required=True)
    new_password_2 = serializers.CharField(required=True)


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = '__all__'
