# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-09-27 14:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20170924_0531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producthistoricindexing',
            name='indexed_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]