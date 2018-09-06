# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('YAAS', '0004_auto_20141014_2313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='min_price',
            field=models.CharField(max_length=20),
        ),
    ]
