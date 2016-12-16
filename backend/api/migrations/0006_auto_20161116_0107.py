# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20161114_1928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='education',
            name='aggregate',
            field=models.CharField(max_length=255),
        ),
    ]
