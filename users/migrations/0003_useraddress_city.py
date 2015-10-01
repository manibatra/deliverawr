# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20151001_1055'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraddress',
            name='city',
            field=models.CharField(max_length=20, default=datetime.datetime(2015, 10, 1, 11, 29, 36, 695144, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
