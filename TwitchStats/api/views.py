from base64 import b64decode

from django.contrib.auth import authenticate
from django.http import JsonResponse, HttpResponse
from rest_framework import status
from .auth import create_token


def login(request):
    params = request.META["QUERY_STRING"]
    params = dict([i.split('=') for i in params.split("&")])
    user = authenticate(username=params["username"], password=params["password"])
    if user is not None:
        access_token = create_token(user)
        return JsonResponse({"access_token": access_token.token, "expiration_at": access_token.expiration_date})
    return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
