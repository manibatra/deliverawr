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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('day', models.CharField(max_length=2, choices=[('Mo', 'Monday'), ('Tu', 'Tuesday'), ('We', 'Wednesday'), ('Th', 'Thursday'), ('Fr', 'Friday'), ('Sa', 'Saturday'), ('Su', 'Sunday')])),
                ('open_hour', models.TimeField()),
                ('close_hour', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='DeliveryLocation',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('postcode', models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('item_id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('price', models.DecimalField(max_digits=5, decimal_places=2)),
                ('description', models.CharField(blank=True, max_length=140)),
                ('category', models.CharField(blank=True, max_length=30)),
                ('time_available', models.CharField(blank=True, max_length=15)),
                ('option_category', models.CharField(blank=True, max_length=30)),
                ('ingredient', models.BooleanField()),
                ('add_on', models.BooleanField()),
                ('removable', models.BooleanField()),
                ('choose_one', models.BooleanField()),
                ('option', models.ForeignKey(blank=True, null=True, to='restaurants.MenuItem', related_name='has_options')),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('restaurant_id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=70)),
                ('street_address', models.CharField(max_length=100)),
                ('postcode', models.CharField(max_length=8)),
                ('country', models.CharField(max_length=20)),
                ('phone_no', models.CharField(max_length=15)),
                ('primary_image', models.ImageField(upload_to='restaurants/primary_image/')),
                ('secondary_image', models.ImageField(upload_to='restaurants/secondary_image/')),
            ],
        ),
        migrations.AddField(
            model_name='menuitem',
            name='restaurant',
            field=models.ForeignKey(related_name='menu_items', to='restaurants.Restaurant'),
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
