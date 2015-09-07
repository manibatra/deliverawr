# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryHours',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('day', models.CharField(max_length=2, unique=True, choices=[('Mo', 'Monday'), ('Tu', 'Tuesday'), ('We', 'Wednesday'), ('Th', 'Thursday'), ('Fr', 'Friday'), ('Sa', 'Saturday'), ('Su', 'Sunday')])),
                ('open_hour', models.TimeField()),
                ('close_hour', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='DeliveryLocation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('postcode', models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('item_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('price', models.DecimalField(decimal_places=2, max_digits=3)),
                ('description', models.CharField(max_length=140)),
                ('category', models.CharField(max_length=30)),
                ('time_available', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Options',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=35)),
                ('ingredient', models.BooleanField()),
                ('add_on', models.BooleanField()),
                ('removable', models.BooleanField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=3)),
                ('item', models.ForeignKey(to='restaurants.MenuItem')),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('restaurant_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=70)),
                ('street_address', models.CharField(max_length=100)),
                ('postcode', models.CharField(max_length=8)),
                ('country', models.CharField(max_length=20)),
                ('phone_no', models.CharField(max_length=15)),
            ],
        ),
        migrations.AddField(
            model_name='menuitem',
            name='restaurant',
            field=models.ForeignKey(to='restaurants.Restaurant'),
        ),
        migrations.AddField(
            model_name='deliverylocation',
            name='restaurant',
            field=models.ForeignKey(to='restaurants.Restaurant'),
        ),
        migrations.AddField(
            model_name='deliveryhours',
            name='restaurant',
            field=models.ForeignKey(to='restaurants.Restaurant'),
        ),
    ]
