'''
util methods for users
'''
import http
import json
import re

from django.http import HttpResponse, HttpResponseNotFound
from django.template import loader

import requests
from decouple import config

from users.models import User


CLIENT_ID = config('CLIENT_ID', default=None)
CLIENT_SECRET = config('CLIENT_SECRET', default=None)


def callback_github(request):
    '''
    Recieve callback from github. Input should be in the format:
    {"code": "1234abcd"}
    '''
    code = request.GET.get('code', None)
    if code:
        req = requests.post(
            'https://github.com/login/oauth/access_token',
            data={
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'code': code,
            },
        )
        token = re.findall(r'^access_token=(\w+)', req.text)

    if token:
        token = token[0]
        req = requests.get(
            'https://api.github.com/user',
            headers={
                'Authorization': f'token {token}',
                'Accept': 'application/vnd.github.v3+json'
            },
        )
        if req.status_code == http.HTTPStatus.OK:
            json_data = json.loads(req.text)
            try:
                user = User.objects.get(github_id=json_data['id'])
                user.email = json_data['email']
                user.username = json_data['login']
                user.avatar = json_data['avatar_url']
                user.github_token = token
                user.save()
            except User.DoesNotExist:
                user = User.objects.create_user(
                    json_data['email'],
                    github_id=json_data['id'],
                    username=json_data['login'],
                    avatar=json_data['avatar_url'],
                    github_token=token,
                )

            template = loader.get_template('../templates/rootapp/home.html')
            context = {
                'token': token,
            }
        return HttpResponse(template.render(context, request))

    return HttpResponseNotFound()


def validate_github_token(request):
    '''
    Receives the token by param ?token=1234abcd,
    validates it and the user,
    still update the user data
    '''
    token = request.GET.get('token', None)

    if token:
        try:
            user = User.objects.get(github_token=token)

            req = requests.get(
                'https://api.github.com/user',
                headers={
                    'Authorization': f'token {token}',
                    'Accept': 'application/vnd.github.v3+json'
                },
            )

            if req.status_code == http.HTTPStatus.OK:
                json_data = json.loads(req.text)
                user.email = json_data['email']
                user.username = json_data['login']
                user.avatar = json_data['avatar_url']
                user.save()
                return HttpResponse(status=204)

        except User.DoesNotExist:
            pass

    return HttpResponse(status=404)


def check_for_github_commits(request):
    commits = request.user.repository_set.prefetch_related('commit').exclude(
        commit__isnull=True).count()
    if commits > 0:
        return HttpResponse(status=204)

    return HttpResponseNotFound()
