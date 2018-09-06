# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('YAAS', '0010_auto_20141101_1228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='min_price',
            field=models.FloatField(max_length=20),
        ),
    ]
