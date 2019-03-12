import http
import json

from django.db import IntegrityError
from django.http import HttpResponse

import requests
from rest_framework.exceptions import NotFound
from rest_framework.pagination import CursorPagination
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Commit, Repository
from .serializers import CommitSerializer, RepositorySerializer
from .tasks import recover_commits, subscribe_on_repo


class IsCreateOrIsAuthenticated(BasePermission):
    """
    permission to create_only
    """
    def has_permission(self, request, view):
        if view.action == 'create':
            return True

        return IsAuthenticated.has_permission(self, request, view)


class RepositoryViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    serializer_class = RepositorySerializer

    def get_queryset(self):
        return Repository.objects.filter(user=self.request.user)

    def perform_create(self, serializer):

        # TODO: CHECK USER NAME

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

            # TODO: Check Date for 30 days
            recover_commits(saved.id)
            subscribe_on_repo.delay(saved.id)

            return saved

        raise NotFound(
            detail="This Repository doesn't exists or you don't have permission to access it",
            code=http.HTTPStatus.NOT_FOUND
        )


class CommitViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    serializer_class = CommitSerializer
    permission_classes = (IsCreateOrIsAuthenticated,)
    pagination_class = CursorPagination
    filter_fields = ['repository', 'repository__id']

    def get_queryset(self):
        return Commit.objects.all().filter(repository__user=self.request.user)

    def create(self, request, *args, **kwargs):
        payload = request.POST.dict().get('payload', None)
        if not payload:
            HttpResponse(status=http.HTTPStatus.UNPROCESSABLE_ENTITY)
        print(f"payload: {payload}")
        print(f"request.data: {request.data}")
        print(f"request.data.get: {request.data.get('commits')}")
        commits = payload.get('commits', None)
        print(f"commits: {commits}")
        repo = payload.get('repository', None)

        if commits and repo:
            try:
                repo = Repository.objects.get(github_id=repo['id'])
            except Repository.DoesNotExist:
                HttpResponse(status=http.HTTPStatus.NOT_FOUND)

            for commit in commits:
                if Commit.objects.filter(sha=commit['id']).exists():
                    continue
                try:
                    commit = Commit(
                        sha=commit['id'],
                        url=commit['url'],
                        author=commit['author'],
                        created=commit['timestamp'],
                        message=commit.get('message', None),
                        repository=repo,
                    )
                    commit.save()
                except IntegrityError:
                    HttpResponse(status=http.HTTPStatus.UNPROCESSABLE_ENTITY)
        else:
            HttpResponse(status=http.HTTPStatus.UNPROCESSABLE_ENTITY)

        return HttpResponse(status=http.HTTPStatus.NO_CONTENT)
