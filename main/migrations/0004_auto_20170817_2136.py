# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-17 21:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_product_marketplace'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='keywords',
            name='product',
        ),
        migrations.AddField(
            model_name='keywords',
            name='historic',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='historic_keywords', to='main.ProductHistoricIndexing'),
        ),
    ]
