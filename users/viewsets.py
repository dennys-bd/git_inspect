'''
ViewSets for users app
'''
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ViewSet

from .utils import callback_github, check_for_github_commits, validate_github_token


class UserViewSet(ViewSet):

    def get_permissions(self):
        '''
        Instantiates and returns the list of permissions that this view requires.
        '''
        if self.action == 'check_for_commits':
            permission_classes = (IsAuthenticated,)
        else:
            permission_classes = (AllowAny,)
        return [permission() for permission in permission_classes]

    @action(detail=False)
    def callback(self, request):
        return callback_github(request)

    @action(detail=False)
    def verify_token(self, request):
        return validate_github_token(request)

    @action(detail=False)
    def check_commits(self, request):
        return check_for_github_commits(request)
