# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-12-03 16:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('referrals', '0001_initial'),
        ('main', '0013_auto_20170929_1945'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='billing_address',
        ),
        migrations.AddField(
            model_name='profile',
            name='referral',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='referrals.Referral'),
        ),
    ]
