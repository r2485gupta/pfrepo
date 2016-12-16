# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_remove_work_freelancer_project_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='work',
            name='freelancer_project_year',
            field=models.CharField(default='2016', max_length=4),
        ),
    ]
