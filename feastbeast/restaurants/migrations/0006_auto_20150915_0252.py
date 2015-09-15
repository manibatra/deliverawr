# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0005_menuitem_choose_one'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='category',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='description',
            field=models.CharField(max_length=140, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='option',
            field=models.ForeignKey(blank=True, related_name='has_options', null=True, to='restaurants.MenuItem'),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='price',
            field=models.DecimalField(max_digits=5, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='time_available',
            field=models.CharField(max_length=15, null=True, blank=True),
        ),
    ]
