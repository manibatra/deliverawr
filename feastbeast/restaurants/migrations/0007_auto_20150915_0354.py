# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0006_auto_20150915_0252'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='option_category',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='category',
            field=models.CharField(default=2, blank=True, max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='description',
            field=models.CharField(blank=True, max_length=140),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='time_available',
            field=models.CharField(blank=True, max_length=15),
        ),
    ]
