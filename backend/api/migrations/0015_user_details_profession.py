# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20161123_1252'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_details',
            name='profession',
            field=models.CharField(max_length=255, default='None'),
        ),
    ]
