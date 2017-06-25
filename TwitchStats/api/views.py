from base64 import b64decode

from django.contrib.auth import authenticate
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import status

from .auth import get_basic_auth, get_or_create_token


def login(request):
    basic = get_basic_auth(request)
    if basic is not None:
        log = b64decode(bytes(basic,'ascii')).decode('ascii').split(':')
        user = authenticate(username=log[0],password=log[1])
        if user is not None:
            token = get_or_create_token(user)
            return JsonResponse(data={'token':token.hash})
    return HttpResponse(status=status.HTTP_400_BAD_REQUEST)