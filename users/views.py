from django.shortcuts import render  # noqa
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.http import HttpRequest
from decouple import config

import requests

from .serializers import UserSerializer

CLIENT_ID = config('CLIENT_ID', default=None)
CLIENT_SECRET = config('CLIENT_SECRET', default=None)


@api_view(['GET'])
@permission_classes([AllowAny])
def callback(request):
    '''
    Recieve callback from github. Input should be in the format:
    {"code": "1234abcd"}
    '''
    # serializer = UserSerializer(data=request.data)
    # code = {request.GET.get('code', '')}
    # if code is not '':
    #     req = requests.get('https://github.com/login/oauth/access_token',
    #                        data={
    #                            'client_id': CLIENT_ID,
    #                            'redirect_uri': 'http://localhost:8000/callback/',
    #                            'client_secret': CLIENT_SECRET,
    #                            'code': code
    #                        })

    # req = {requests.GET.get('')}

    # print('final')
    # print(req)
    # oauth_token = request.GET.get("token")
    # print(oauth_token)

    return Response(request.GET)



    # if serializer.is_valid():
    #     serializer.save()

    #     r = requests.post('http://0.0.0.0:8000/o/token/',
    #         data={
    #             'grant_type': 'code',
    #             'username': request.data['username'],
    #             'code': request.data['code'],
    #             'client_id': CLIENT_ID,
    #             'client_secret': CLIENT_SECRET,
    #         },
    #     )
    #     return Response(r.json())
    # return Response(serializer.errors)

@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    '''
    Gets tokens with username and password. Input should be in the format:
    {"username": "username", "password": "1234abcd"}
    '''
    r = requests.post(
    'http://0.0.0.0:8000/o/token/',
        data={
            'grant_type': 'code',
            'username': request.data['username'],
            'code': request.data['code'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
    )
    return Response(r.json())

@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    '''
    Registers user to the server. Input should be in the format:
    {"refresh_token": "<token>"}
    '''
    r = requests.post(
    'http://0.0.0.0:8000/o/token/',
        data={
            'grant_type': 'refresh_token',
            'refresh_token': request.data['refresh_token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
    )
    return Response(r.json())

@api_view(['POST'])
@permission_classes([AllowAny])
def revoke_token(request):
    '''
    Method to revoke tokens.
    {"token": "<token>"}
    '''
    r = requests.post(
        'http://0.0.0.0:8000/o/revoke_token/',
        data={
            'token': request.data['token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
    )
    if r.status_code == 200:
        return Response({'message': 'token revoked'}, r.status_code)
    return Response(r.json(), r.status_code)
