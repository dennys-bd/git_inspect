"""
    OAuth Related Views
"""
# from rest_framework.response import Response
import re
import json
import http
import requests

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.http import HttpResponseNotFound, HttpResponse
from django.template import loader
from decouple import config

from users.models import User


CLIENT_ID = config('CLIENT_ID', default=None)
CLIENT_SECRET = config('CLIENT_SECRET', default=None)

@api_view(['GET'])
@permission_classes([AllowAny])
def callback(request):
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
            user = User.objects.get(email=json_data['email'])

            if user:
                user.github_token = token
                user.save()
            else:
                user = User.objects().create_user(json_data['email'], github_token=token)

            template = loader.get_template('../templates/loginapp/login.html')
            context = {
                'token': token,
            }
        return HttpResponse(template.render(context, request))

    return HttpResponseNotFound()

