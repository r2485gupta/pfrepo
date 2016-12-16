# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20161123_1051'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='certification',
            name='title',
        ),
        migrations.RemoveField(
            model_name='patent',
            name='title',
        ),
        migrations.RemoveField(
            model_name='publication',
            name='title',
        ),
        migrations.RemoveField(
            model_name='work',
            name='freelancer_project_details',
        ),
        migrations.RemoveField(
            model_name='work',
            name='intership_roles_responsibilities',
        ),
        migrations.RemoveField(
            model_name='work',
            name='job_roles_and_responsibilities',
        ),
    ]
