# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('YAAS', '0006_auto_20141015_1727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='starting_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
