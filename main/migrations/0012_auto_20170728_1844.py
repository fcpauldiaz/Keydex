# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-28 18:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_producthistoricindexing'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='producthistoricindexing',
            table='main_product_historic_indexing',
        ),
    ]
