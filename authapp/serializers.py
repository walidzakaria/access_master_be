from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from .models import *



class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'password', 'first_name', 'last_name',)


class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name',)


class UserInfoSerializer(serializers.ModelSerializer):
    user_type = serializers.SerializerMethodField()


    def get_user_type(self, obj):
        groups = obj.groups.first()
        if groups:
            return groups.name
        return 'employee'

    class Meta:
        model = User
        fields = ('id', 'user_type', 'last_login', 'username', 'first_name', 'last_name',
                  'email', 'user_type', 'groups',)
