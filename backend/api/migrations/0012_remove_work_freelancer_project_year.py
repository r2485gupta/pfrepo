# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20161123_1159'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='work',
            name='freelancer_project_year',
        ),
    ]
