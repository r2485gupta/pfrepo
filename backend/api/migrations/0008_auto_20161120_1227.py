# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_remove_skills_soft_skills'),
    ]

    operations = [
        migrations.RenameField(
            model_name='skills',
            old_name='technical_skills',
            new_name='skill_name',
        ),
    ]
