# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='primary_image',
            field=models.ImageField(upload_to='restaurant/primary_image/', default=datetime.datetime(2015, 9, 9, 15, 2, 13, 591511, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='secondary_image',
            field=models.ImageField(upload_to='restaurant/secondary_image/', default=datetime.datetime(2015, 9, 9, 15, 2, 25, 286927, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
