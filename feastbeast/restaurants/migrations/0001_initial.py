# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('item_id', models.AutoField(serialize=False, primary_key=True)),
                ('menu_id', models.IntegerField()),
                ('item_name', models.CharField(max_length=30)),
                ('item_price', models.IntegerField()),
                ('item_description', models.CharField(max_length=140)),
                ('item_category', models.CharField(max_length=30)),
            ],
        ),
    ]
