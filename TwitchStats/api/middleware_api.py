import re
from django.http.response import HttpResponse
from .models import AccessToken


class MiddlewareAPI(object):

    def process_request(self, request):
        if re.search(r"^/api/v1/", request.path) is not None and re.search(r"^/api/v1/login", request.path) is None:
            params = request.META["QUERY_STRING"]
            if len(params) > 0:
                params = dict([i.split('=') for i in params.split("&")])
                if "access_token" in params:
                    token = params['access_token']
                    access_token = AccessToken.objects.filter(token=token).first()
                    if access_token is not None and access_token.is_expired() is False:
                        return None
            return HttpResponse('Unauthorized', status=401)



