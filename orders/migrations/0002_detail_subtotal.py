# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='detail',
            name='subtotal',
            field=models.DecimalField(max_digits=10, default=0.0, decimal_places=2),
            preserve_default=False,
        ),
    ]
