# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('YAAS', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='auction',
            options={},
        ),
        migrations.RemoveField(
            model_name='auction',
            name='end_date',
        ),
        migrations.AddField(
            model_name='auction',
            name='category',
            field=models.CharField(max_length=20, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='auction',
            name='status',
            field=models.CharField(max_length=20, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='auction',
            name='description',
            field=models.TextField(max_length=100),
        ),
        migrations.AlterField(
            model_name='auction',
            name='seller',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='auction',
            name='starting_date',
            field=models.DateTimeField(null=True),
        ),
    ]
