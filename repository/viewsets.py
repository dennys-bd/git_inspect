from rest_framework.viewsets import ModelViewSet
from repository.models import Repository, Commit
from .serializers import RepositorySerializer, CommitSerializer

class RepositoryViewSet(ModelViewSet):
    serializer_class = RepositorySerializer

    def get_queryset(self):
        return Repository.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class CommitViewSet(ModelViewSet):
    serializer_class = CommitSerializer

    def get_queryset(self):
        return Commit.objects.all()
