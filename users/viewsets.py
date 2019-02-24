# from rest_framework import status
from rest_framework import permissions, viewsets
# from rest_framework.decorators import action, authentication_classes, permission_classes
# from rest_framework.response import Response
from django.contrib.auth.models import Group
# from django.shortcuts import get_object_or_404
from .models import User
from .serializers import GroupSerializer, UserSerializer

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope

class GroupViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, TokenHasScope,)

    def get_serializer_class(self):
        return GroupSerializer

    def get_queryset(self):
        return Group.objects.all()

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, TokenHasReadWriteScope,)

    def get_serializer_class(self):
        return UserSerializer

    def get_queryset(self):
        return User.objects.all()
