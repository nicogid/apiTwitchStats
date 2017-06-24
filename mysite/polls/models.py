from django.utils import timezone
import datetime

from django.db import models


def get_expiration_date():
    return timezone.now() + datetime.timedelta(days=1)


class Token(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, unique=True)
    hash = models.CharField(max_length=100)
    expiration_date = models.DateTimeField(default=get_expiration_date)

    def is_expired(self):
        return self.expiration_date < timezone.now()


class User(models.Model):
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    password = models.CharField(max_length=20)


class Game(models.Model):
    url_image = models.CharField(max_length=100)
    name = models.CharField(max_length=20)
    channels = models.IntegerField()
    viewers = models.IntegerField()
    popularity = models.IntegerField()


class Channel(models.Model):
    # a modifier selon la foreign key
    #id_channel = models.ForeignKey(Channel)
    logo = models.CharField(max_length=50)
    name = models.CharField(max_length=20)
    url = models.CharField(max_length=50)
    view = models.IntegerField()


class Video(models.Model):
    # a modifier selon la foreign key
    #id_twitch = models.ForeignKey(Game)
    id_channel = models.ForeignKey(Channel)
    game = models.CharField(max_length=10)
    viewers = models.IntegerField()
    created_at = models.DateTimeField()


class Message(models.Model):
    id_user = models.ForeignKey(User)
    body = models.CharField(max_length=20)
    created_at = models.DateTimeField()
