# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('YAAS', '0005_auto_20141015_0037'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='auction_winner',
            field=models.CharField(max_length=20, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='auction',
            name='current_bidder',
            field=models.CharField(max_length=20, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='auction',
            name='end_date',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
    ]
