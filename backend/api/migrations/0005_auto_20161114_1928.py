# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20161114_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='work',
            name='internship_date_from',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='work',
            name='internship_date_to',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='work',
            name='job_date_from',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='work',
            name='job_date_to',
            field=models.DateField(blank=True, null=True),
        ),
    ]
