# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Detail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('add_ons', models.ManyToManyField(related_name='added_items', to='restaurants.MenuItem')),
                ('menu_item', models.ForeignKey(related_name='menu_item', to='restaurants.MenuItem')),
            ],
        ),
        migrations.CreateModel(
            name='UserOrder',
            fields=[
                ('order_id', models.AutoField(serialize=False, primary_key=True)),
                ('order_time', models.DateTimeField(auto_now_add=True)),
                ('total_price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('delivery_address', models.ForeignKey(related_name='delivered_to', to='users.UserAddress')),
                ('restaurant', models.ForeignKey(related_name='ordered_from', to='restaurants.Restaurant')),
                ('user', models.ForeignKey(related_name='ordered_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='detail',
            name='order',
            field=models.ForeignKey(related_name='order_number', to='orders.UserOrder'),
        ),
        migrations.AddField(
            model_name='detail',
            name='removed',
            field=models.ManyToManyField(related_name='removed_items', to='restaurants.MenuItem'),
        ),
    ]
