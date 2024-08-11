from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class TokenSerializer(serializers.ModelSerializer):
    token = serializers.CharField(source='key')

    class Meta:
        model = Token
        fields = ['token']


class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    is_superuser = serializers.BooleanField()
    groups = serializers.ListField()
    permissions = serializers.ListField()

    def to_representation(self, instance: User):
        return {
            'username': instance.username,
            'is_superuser': instance.is_superuser,
            'groups': instance.groups.all().values_list('name', flat=True),
            'permissions': instance.get_all_permissions()
        }
