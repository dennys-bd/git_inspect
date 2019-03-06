import http
import json

from django.http import HttpResponse

import requests
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Commit, Repository
from .serializers import CommitSerializer, RepositorySerializer
from .tasks import recover_commits, subscribe_on_repo


class RepositoryViewSet(ModelViewSet):
    serializer_class = RepositorySerializer

    def get_queryset(self):
        return Repository.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        req = requests.get(
            f'https://api.github.com/repos/{serializer.validated_data["name"]}',
            headers={
                'Authorization': f'token {self.request.user.github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
        )

        if req.status_code == http.HTTPStatus.OK:
            json_data = json.loads(req.text)
            serializer.validated_data['name'] = json_data['name']
            serializer.validated_data['url'] = json_data['html_url']
            serializer.validated_data['description'] = json_data['description']
            serializer.validated_data['github_id'] = json_data['id']

            saved = serializer.save(user=self.request.user)

            recover_commits(saved.id)
            subscribe_on_repo.delay(saved.id)

        return saved

class CommitViewSet(ModelViewSet):
    serializer_class = CommitSerializer

    def get_permissions(self):

        if self.action == 'create':
            return [AllowAny]
        else:
            return [IsAuthenticated]

    def get_queryset(self):
        return Commit.objects.order_by_date()

    def create(self, request, *args, **kwargs):
        print(f'PARAMS: {request.POST}')
        return HttpResponse(status=204)
