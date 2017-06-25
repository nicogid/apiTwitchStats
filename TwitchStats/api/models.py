from django.utils import timezone
import datetime

from django.db import models


def get_expiration_date():
    return timezone.now() + datetime.timedelta(days=1)


class VersionPull(models.Model):
    status = models.CharField(max_length=20)
    percent = models.FloatField()
    client_id = models.CharField(max_length=255, null=True)


class Token(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, unique=True)
    hash = models.CharField(max_length=100)
    expiration_date = models.DateTimeField(default=get_expiration_date)

    def is_expired(self):
        return self.expiration_date < timezone.now()


class User(models.Model):
    id_user_twitch = models.IntegerField(unique=True)
    name = models.CharField(max_length=255, null=True)
    logo = models.CharField(max_length=255, null=True)
    bio = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name


class Game(models.Model):
    id_game_twitch = models.IntegerField(unique=True)
    url_image = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255)
    viewers = models.IntegerField(null=True)
    popularity = models.IntegerField(null=True)

    def __str__(self):
        return self.name


class Channel(models.Model):
    id_channel_twitch = models.IntegerField(unique=True)
    created_at = models.DateTimeField()
    logo = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255, null=True)
    url = models.CharField(max_length=255, null=True)
    nb_views = models.IntegerField(null=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    #class Meta:
    #    unique_together = ('id_channel_twitch', 'id_game')


class Video(models.Model):
    id_video_twitch = models.CharField(max_length=50, unique=True)
    url = models.CharField(max_length=250)
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=250, null=True)
    game = models.ForeignKey(Game)
    channel = models.ForeignKey(Channel)
    nb_views = models.IntegerField(null=True)
    created_at = models.DateTimeField(null=True)
    recorded_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.title


class Message(models.Model):
    id_message_twitch = models.CharField(max_length=255, unique=True)
    video = models.ForeignKey(Video)
    user = models.ForeignKey(User)
    body = models.CharField(max_length=500)
    timestamp = models.IntegerField(null=False)

    def __str__(self):
        return self.body
