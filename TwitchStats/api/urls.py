from . import views
from django.conf.urls import include
from django.conf.urls import url
from rest_framework import routers
from .serializer import ChannelViewSet, GameViewSet, \
    VideoViewSet, MessageViewSet, UserViewSet, \
    VideoList, MessageList

router = routers.DefaultRouter()
router.register(r'v1/users', UserViewSet)
router.register(r'v1/videos', VideoViewSet)
router.register(r'v1/games', GameViewSet)
router.register(r'v1/messages', MessageViewSet)
router.register(r'v1/channels', ChannelViewSet)

urlpatterns = [
    url(r'^login$', views.login, name='login'),
    url(r'^/v1/videos/game/(?P<game>[a-z0-9]+)/?$', VideoList.as_view()),
    url(r'^v1/messages/video/(?P<video>[a-z0-9]+)/?$', MessageList.as_view()),
    url(r'^', include(router.urls)),
]