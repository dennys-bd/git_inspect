from django.http import Http404

from rest_framework.permissions import BasePermission, IsAuthenticated


class IsAuthenticatedOr404(BasePermission):
    def has_permission(self, request, view):
        if IsAuthenticated.has_permission(self, request, view):
            return True

        raise Http404


class IsCreateOrIsAuthenticatedOr404(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            return True

        return IsAuthenticatedOr404.has_permission(self, request, view)
