# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20170625_1422'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='video',
            field=models.ForeignKey(to='api.Video', default=None),
            preserve_default=False,
        ),
    ]
