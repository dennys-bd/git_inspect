'''
utils methods for repositories
'''
import http
import json

from django.db import IntegrityError
from django.http import HttpResponse

import requests
from rest_framework.exceptions import NotFound

from .models import Commit, Repository
from .tasks import recover_commits, subscribe_on_repo


def create_from_dict(dct, model):
    '''
    This function recieves a dictionary and creates a model from it, ignoring fields that are not
    in the model.
    '''
    fields = set(f.name for f in model._meta.get_fields())
    dct = {k: v for k, v in dct.items() if k in fields}
    return model(**dct)


def create_commit(request):
    '''
    Creates a new commit from request.
    '''
    payload = request.POST.dict().get('payload', None)

    if not payload:
        return HttpResponse(status=http.HTTPStatus.UNPROCESSABLE_ENTITY)

    payload = json.loads(payload)

    commits = payload.get('commits', None)
    repo = payload.get('repository', None)

    if not (commits and repo):
        return HttpResponse(status=http.HTTPStatus.UNPROCESSABLE_ENTITY)

    try:
        repo = Repository.objects.get(github_id=repo['id'])
    except Repository.DoesNotExist:
        return HttpResponse(status=http.HTTPStatus.NOT_FOUND)

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
            return HttpResponse(status=http.HTTPStatus.UNPROCESSABLE_ENTITY)

    return HttpResponse(status=http.HTTPStatus.NO_CONTENT)


def create_repo(request, serializer):
    '''
    Creates a new repo from serializers request.
    '''
    # TODO: CHECK USER NAME

    req = requests.get(
        f'https://api.github.com/repos/{serializer.validated_data["name"]}',
        headers={
            'Authorization': f'token {request.user.github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
    )

    if req.status_code == http.HTTPStatus.OK:
        json_data = json.loads(req.text)
        serializer.validated_data['name'] = json_data['name']
        serializer.validated_data['url'] = json_data['html_url']
        serializer.validated_data['description'] = json_data['description']
        serializer.validated_data['github_id'] = json_data['id']

        try:
            saved = serializer.save(user=request.user)
        except IntegrityError:
            raise NotFound(
                detail="You have already added this repository",
                code=http.HTTPStatus.UNPROCESSABLE_ENTITY
            )

        recover_commits(saved.id)
        subscribe_on_repo.delay(saved.id)

        return saved

    raise NotFound(
        detail="This Repository doesn't exists or you don't have permission to access it",
        code=http.HTTPStatus.NOT_FOUND
    )
