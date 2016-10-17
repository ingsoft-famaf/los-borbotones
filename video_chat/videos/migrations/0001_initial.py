# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-17 21:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=300)),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='date_published')),
            ],
        ),
    ]