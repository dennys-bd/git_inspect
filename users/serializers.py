from rest_framework import serializers
from .models import User
from django.contrib.auth.models import Group

class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = User.objects.get_or_create(**validated_data)
        return user

    class Meta:
        model = User
        fields = ('id', 'email')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("name", )
