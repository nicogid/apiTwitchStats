from .parse_twitch import ParseTwitch
from django.contrib import admin


# Register your models here.

from .models import User, Video, Game, Channel, VersionPull, Message
from django.shortcuts import render
from django.http import JsonResponse


def process_pull_twitch(request, *args, **kwargs):
    version = VersionPull.objects.last()
    p = ParseTwitch(version)
    p.parse_and_save()
    version.percent = 100
    version.status = "success"
    version.save()
    return JsonResponse({'id': version.id, 'status': version.status,
                         'percent': version.percent})

admin.site.register_view('pull/process', view=process_pull_twitch, visible=False)


def get_info_pull_twitch(request, id_version):
    version = VersionPull.objects.get(id=id_version)
    return JsonResponse({'id': version.id, 'status': version.status,
                         'percent': version.percent})

admin.site.register_view('pull/version/info/(?P<id_version>[0-9]+)', view=get_info_pull_twitch, visible=False)


def pull_twitch(request, *args, **kwargs):
    if request.method == "POST":
        version = VersionPull(status="pending", percent=0)
        version.client_id = request.POST.get('client_id', '')
        version.save()
        return JsonResponse({'id': version.id}, status=201)

    return render(request, 'admin/pull.html')


admin.site.register_view('pull/twitch', 'Pull Twitch', view=pull_twitch)


admin.site.register(User)
admin.site.register(Video)
admin.site.register(Game)
admin.site.register(Channel)
admin.site.register(Message)
