# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('restaurants', '0007_auto_20150915_0354'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('add_ons', models.ManyToManyField(to='restaurants.MenuItem', related_name='add_ons')),
                ('menu_item', models.ForeignKey(to='restaurants.MenuItem', related_name='menu_item')),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('total', models.DecimalField(max_digits=10, decimal_places=2)),
                ('completed_datetime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderStatus',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('is_completed', models.BooleanField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='orders',
            name='order',
            field=models.ForeignKey(to='orders.OrderStatus', related_name='order'),
        ),
        migrations.AddField(
            model_name='orders',
            name='restaurant',
            field=models.ForeignKey(to='restaurants.Restaurant', related_name='restaurant_order'),
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='order',
            field=models.ForeignKey(to='orders.OrderStatus', related_name='order_number'),
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='removed',
            field=models.ManyToManyField(to='restaurants.MenuItem', related_name='removed_items'),
        ),
    ]
