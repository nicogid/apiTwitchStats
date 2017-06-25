# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import api.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('id_channel_twitch', models.IntegerField(unique=True)),
                ('created_at', models.DateTimeField()),
                ('logo', models.CharField(max_length=255, null=True)),
                ('name', models.CharField(max_length=255, null=True)),
                ('url', models.CharField(max_length=255, null=True)),
                ('nb_views', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('id_game_twitch', models.IntegerField(unique=True)),
                ('url_image', models.CharField(max_length=255, null=True)),
                ('name', models.CharField(max_length=255)),
                ('viewers', models.IntegerField(null=True)),
                ('popularity', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('id_message_twitch', models.IntegerField(unique=True)),
                ('body', models.CharField(max_length=500)),
                ('created_at', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('hash', models.CharField(max_length=100)),
                ('expiration_date', models.DateTimeField(default=api.models.get_expiration_date)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('id_user_twitch', models.IntegerField(unique=True)),
                ('name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('bio', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='VersionPull',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('status', models.CharField(max_length=20)),
                ('percent', models.IntegerField()),
                ('client_id', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('id_video_twitch', models.CharField(unique=True, max_length=50)),
                ('url', models.CharField(max_length=250)),
                ('title', models.CharField(max_length=250)),
                ('description', models.CharField(max_length=250, null=True)),
                ('nb_views', models.IntegerField(null=True)),
                ('created_at', models.DateTimeField(null=True)),
                ('channel', models.ForeignKey(to='api.Channel')),
                ('game', models.ForeignKey(to='api.Game')),
            ],
        ),
        migrations.AddField(
            model_name='token',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='message',
            name='user',
            field=models.ForeignKey(to='api.User'),
        ),
        migrations.AddField(
            model_name='channel',
            name='game',
            field=models.ForeignKey(to='api.Game'),
        ),
    ]
