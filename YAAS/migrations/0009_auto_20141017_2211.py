# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('YAAS', '0008_auto_20141016_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='description',
            field=models.TextField(),
        ),
    ]
