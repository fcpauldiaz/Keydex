# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-26 18:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20170726_1823'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='crawl_time',
        ),
    ]
