# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2021-04-08 08:08
from __future__ import unicode_literals

import collectionfield.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0006_useranswer_answer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useranswer',
            name='answer',
            field=collectionfield.models.fields.CollectionField(),
        ),
    ]
