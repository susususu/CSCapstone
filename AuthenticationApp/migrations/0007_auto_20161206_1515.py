# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-06 20:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AuthenticationApp', '0006_auto_20161204_1751'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='university',
        ),
        migrations.AddField(
            model_name='student',
            name='about',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='contact',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='teacher',
            name='about',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
