# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-02 05:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AuthenticationApp', '0004_auto_20161128_2024'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='engineer',
            name='university',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='university',
        ),
    ]
