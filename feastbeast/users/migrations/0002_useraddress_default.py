# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraddress',
            name='default',
            field=models.BooleanField(default=datetime.datetime(2015, 9, 12, 14, 5, 1, 467966, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
