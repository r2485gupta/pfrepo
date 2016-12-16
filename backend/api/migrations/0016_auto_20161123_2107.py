# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_user_details_profession'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_details',
            name='first_name',
            field=models.CharField(max_length=255, default='None'),
        ),
        migrations.AddField(
            model_name='user_details',
            name='last_name',
            field=models.CharField(max_length=255, default='None'),
        ),
    ]
