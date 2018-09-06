# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Auction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('seller', models.CharField(max_length=20)),
                ('title', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=100)),
                ('min_price', models.IntegerField()),
                ('starting_date', models.DateTimeField(default=datetime.datetime(2014, 10, 13, 16, 51, 17, 744000))),
                ('end_date', models.DateTimeField()),
            ],
            options={
                'ordering': ['starting_date'],
            },
            bases=(models.Model,),
        ),
    ]
