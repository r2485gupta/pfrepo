# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20161116_0107'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='skills',
            name='soft_skills',
        ),
    ]
