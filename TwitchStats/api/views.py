from base64 import b64decode

from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import ParseError

from TwitchStats.api.serializer import UserSerializer
from .auth import get_basic_auth, get_or_create_token

@csrf_exempt
def login(request):
    basic = get_basic_auth(request)
    if basic is not None:
        log = b64decode(bytes(basic,'ascii')).decode('ascii').split(':')
        user = authenticate(username=log[0],password=log[1])
        if user is not None:
            token = get_or_create_token(user)
            return JsonResponse(data={'token':token.hash})
    return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

def create_user(request):
    try:
        data = JSONParser().parse(request)
    except ParseError:
        return HttpResponse(status=400)
    serializer = UserSerializer(data=data, context={'request': request})
    if serializer.is_valid():
        user = User.objects.create_user(username=data['username'], password=data['password'])
        token = get_or_create_token(user)
        return JsonResponse(data={'token': token.hash})
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def users(request):
    if request.method == 'POST':
        return create_user(request)
    else:
        return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)
