# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2021-04-08 08:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0004_useranswer_answer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useranswer',
            name='answer',
        ),
    ]