"""
    OAuth Related Views
"""
# from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.http import HttpResponse, HttpResponseNotFound
from django.template import loader
from decouple import config

# import requests


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
        template = loader.get_template('../templates/loginapp/login.html')
        context = {
            'code': code,
        }
        return HttpResponse(template.render(context, request))
    return HttpResponseNotFound()
