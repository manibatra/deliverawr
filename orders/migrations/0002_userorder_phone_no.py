# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_userverification'),
        ('orders', '0001_squashed_0002_detail_subtotal'),
    ]

    operations = [
        migrations.AddField(
            model_name='userorder',
            name='phone_no',
            field=models.ForeignKey(to='users.UserPhoneNo', related_name='cus_phone_no', default=''),
            preserve_default=False,
        ),
    ]
