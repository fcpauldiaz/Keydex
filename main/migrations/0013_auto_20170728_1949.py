# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-28 19:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20170728_1844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producthistoricindexing',
            name='indexed_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]