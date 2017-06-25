# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20170625_1315'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='recorded_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='id_message_twitch',
            field=models.CharField(unique=True, max_length=255),
        ),
    ]
