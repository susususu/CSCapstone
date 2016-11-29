# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-29 01:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AuthenticationApp', '0003_student'),
    ]

    operations = [
        migrations.CreateModel(
            name='Engineer',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('university', models.CharField(max_length=100)),
                ('contact', models.CharField(max_length=100)),
                ('about', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('university', models.CharField(max_length=100)),
                ('contact', models.CharField(max_length=100)),
                ('about', models.CharField(max_length=500)),
            ],
        ),
        migrations.AddField(
            model_name='myuser',
            name='is_engineer',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='myuser',
            name='is_professor',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='myuser',
            name='is_student',
            field=models.BooleanField(default=False),
        ),
    ]
