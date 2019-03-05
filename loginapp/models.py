import json
import http
import requests

from rest_framework.authentication import TokenAuthentication, get_authorization_header
from rest_framework import exceptions
from django.utils.translation import ugettext_lazy as _

from users.models import User

class CustomAuthentication(TokenAuthentication):

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        # req = requests.get(
        #     'https://api.github.com/user',
        #     headers={
        #         'Authorization': f'token {}',
        #         'Accept': 'application/vnd.github.v3+json'
        #     },
        # )
        # if req.status_code == http.HTTPStatus.OK:
        #     json_data = json.loads(req.text)

        try:
            user = User.objects.get(github_token=auth[1].decode("utf-8"))
            return (user, None)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid user.'))

