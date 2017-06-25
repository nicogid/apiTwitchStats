from . import views
from django.conf.urls import include
from django.conf.urls import url
from rest_framework import routers, serializers, viewsets
from .serializer import ChannelViewSet, GameViewSet, \
    VideoViewSet, MessageViewSet, UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'videos', VideoViewSet)
router.register(r'games', GameViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'channels', ChannelViewSet)


urlpatterns = [
    url(r'^login$', views.login, name='login'),
    url(r'^users$', views.users, name='user'),
    url(r'^', include(router.urls)),
]