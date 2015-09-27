# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('users', '__first__'),
        ('restaurants', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Detail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('add_ons', models.ManyToManyField(to='restaurants.MenuItem', related_name='added_items')),
                ('menu_item', models.ForeignKey(to='restaurants.MenuItem', related_name='menu_item')),
            ],
        ),
        migrations.CreateModel(
            name='UserOrder',
            fields=[
                ('order_id', models.AutoField(serialize=False, primary_key=True)),
                ('order_time', models.DateTimeField(auto_now_add=True)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('delivery_address', models.ForeignKey(to='users.UserAddress', related_name='delivered_to')),
                ('restaurant', models.ForeignKey(to='restaurants.Restaurant', related_name='ordered_from')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='ordered_by')),
            ],
        ),
        migrations.AddField(
            model_name='detail',
            name='order',
            field=models.ForeignKey(to='orders.UserOrder', related_name='order_number'),
        ),
        migrations.AddField(
            model_name='detail',
            name='removed',
            field=models.ManyToManyField(to='restaurants.MenuItem', related_name='removed_items'),
        ),
    ]
