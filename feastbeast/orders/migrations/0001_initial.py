# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0003_auto_20150909_1513'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('order_id', models.AutoField(serialize=False, primary_key=True)),
                ('total', models.DecimalField(max_digits=10, decimal_places=2)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('menu_items', models.ManyToManyField(to='restaurants.MenuItem')),
                ('restaurant', models.ForeignKey(related_name='restaurant_order', to='restaurants.Restaurant')),
                ('user', models.ForeignKey(related_name='user_order', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
