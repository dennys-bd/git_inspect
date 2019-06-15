'''
ViewSets for repositories app
'''
from rest_framework.pagination import CursorPagination
from rest_framework.viewsets import ModelViewSet

from .models import Commit, Repository
from .permissions import IsCreateOrIsAuthenticatedOr404
from .serializers import CommitSerializer, RepositorySerializer
from .utils import create_commit, create_repo


class RepositoryViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    '''
    Repository ViewSet to resolve the requests to /repositories
    '''
    serializer_class = RepositorySerializer

    def get_queryset(self):
        return Repository.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        return create_repo(self.request, serializer)


class CommitViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    '''
    Commit ViewSet to resolve the requests to /commits
    '''
    serializer_class = CommitSerializer
    permission_classes = (IsCreateOrIsAuthenticatedOr404,)
    pagination_class = CursorPagination
    filter_fields = ['repository', 'repository__id']

    def get_queryset(self):
        return Commit.objects.all().filter(repository__user=self.request.user)

    def create(self, request, *args, **kwargs):
        return create_commit(request)
