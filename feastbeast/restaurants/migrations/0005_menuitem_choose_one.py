# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0004_auto_20150915_0209'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='choose_one',
            field=models.BooleanField(default=datetime.datetime(2015, 9, 15, 2, 31, 47, 383278, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
