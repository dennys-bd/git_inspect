"""
    OAuth Related Views
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from .utils import callback_github, check_for_github_commits, validate_github_token


@api_view(['GET'])
@permission_classes([AllowAny])
def callback(request):
    '''
    GET /callback
    '''
    return callback_github(request)


@api_view(['GET'])
@permission_classes([AllowAny])
def verify_token(request):
    '''
    GET /verify_token
    '''
    return validate_github_token(request)


@api_view(['GET'])
def check_for_commits(request):
    '''
    GET /check_for_commits
    '''
    return check_for_github_commits(request)
