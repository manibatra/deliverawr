# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0002_auto_20150909_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='primary_image',
            field=models.ImageField(upload_to='restaurants/primary_image/'),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='secondary_image',
            field=models.ImageField(upload_to='restaurants/secondary_image/'),
        ),
    ]
