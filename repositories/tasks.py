import datetime
import http
import json

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

import requests
from requests.exceptions import RequestException

from git_inspect.celery import app

from .models import Commit, Repository


@app.task
def recover_commits(repository_id):
    try:
        repo = Repository.objects.select_related().get(id=repository_id)
    except ObjectDoesNotExist:
        return

    since = datetime.date.today() - datetime.timedelta(days=30)
    sincestr = since.strftime('%Y-%m-%D')
    req = requests.get(
        f'https://api.github.com/repos/{repo.full_name}/commits?since={sincestr}',
        headers={
            'Authorization': f'token {repo.user.github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
    )

    if req.status_code == http.HTTPStatus.OK:
        json_data = json.loads(req.text)
        for c_data in json_data:
            try:
                commit = Commit(
                    sha=c_data['sha'],
                    url=c_data['html_url'],
                    author=c_data['commit']['author'],
                    created=c_data['commit']['committer']['date'],
                    message=c_data['commit']['message'],
                    repository=repo,
                )
                commit.save()
            except (TypeError, IntegrityError):
                pass


@app.task(autoretry_for=(RequestException,), default_retry_delay=15 * 60,
          retry_kwargs={'max_retries': 4})
def subscribe_on_repo(repository_id):
    try:
        repo = Repository.objects.select_related().get(id=repository_id)
    except ObjectDoesNotExist:
        return

    req = requests.post(
        f'https://api.github.com/repos/{repo.full_name}/hooks',
        headers={
            'Authorization': f'token {repo.user.github_token}',
            'Accept': 'application/vnd.github.v3+json'
        },
        json={
            'name': 'web',
            'events': [
                'push'
            ],
            'config': {
                'url': 'https://git-inspect.herokuapp.com/commits/'
            }
        }
    )

    if req.status_code == http.HTTPStatus.FORBIDDEN:
        return

    if req.status_code != http.HTTPStatus.CREATED:
        raise RequestException

    json_data = json.loads(req.text)
    Repository.objects.filter(id=repository_id).update(github_hook_id=json_data['id'])
