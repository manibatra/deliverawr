# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0003_auto_20150909_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='add_on',
            field=models.BooleanField(default=datetime.datetime(2015, 9, 15, 2, 9, 12, 572025, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='menuitem',
            name='ingredient',
            field=models.BooleanField(default=datetime.datetime(2015, 9, 15, 2, 9, 20, 819644, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='menuitem',
            name='option',
            field=models.ForeignKey(null=True, related_name='has_options', to='restaurants.MenuItem'),
        ),
        migrations.AddField(
            model_name='menuitem',
            name='removable',
            field=models.BooleanField(default=datetime.datetime(2015, 9, 15, 2, 9, 27, 291469, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='description',
            field=models.CharField(null=True, max_length=140),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='restaurant',
            field=models.ForeignKey(to='restaurants.Restaurant', related_name='menu_items'),
        ),
    ]
