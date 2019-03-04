import json
import http
import requests
import datetime

from rest_framework.viewsets import ModelViewSet
from repository.models import Repository, Commit
from .serializers import RepositorySerializer, CommitSerializer
from django.http import JsonResponse

class RepositoryViewSet(ModelViewSet):
    serializer_class = RepositorySerializer

    def get_queryset(self):
        return Repository.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        req = requests.get(
            f'https://api.github.com/repos/{self.request.user.username}/{serializer.validated_data["name"]}',
            headers={
                'Authorization': f'token {self.request.user.github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
        )

        if req.status_code == http.HTTPStatus.OK:
            json_data = json.loads(req.text)
            serializer.validated_data['url'] = json_data['html_url']
            serializer.validated_data['description'] = json_data['description']
            serializer.validated_data['github_id'] = json_data['id']

            since = datetime.date.today()  - datetime.timedelta(days=30)
            sincestr = since.strftime('%Y-%m-%D')
            # req = requests.get(
            #     f'https://api.github.com/repos/{self.request.user.username}/{serializer.validated_data["name"]}/commits?since={sincestr}',
            #     headers={
            #         'Authorization': f'token {self.request.user.github_token}',
            #         'Accept': 'application/vnd.github.v3+json'
            #     }
            # )

            # if req.status_code == http.HTTPStatus.OK:

            #     json_data = json.loads(req.text)
            #     for i in json_data:

        return serializer.save(user=self.request.user)


class CommitViewSet(ModelViewSet):
    serializer_class = CommitSerializer

    def get_queryset(self):
        return Commit.objects.all()
