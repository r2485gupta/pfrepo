# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20161120_1227'),
    ]

    operations = [
        migrations.AddField(
            model_name='work',
            name='freelancer_project_year',
            field=models.CharField(max_length=4, default='2016'),
        ),
    ]
