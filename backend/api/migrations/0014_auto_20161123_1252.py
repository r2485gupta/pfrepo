# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_work_freelancer_project_year'),
    ]

    operations = [
        migrations.RenameField(
            model_name='work',
            old_name='freelancer_project_year',
            new_name='freelancer_year',
        ),
    ]
