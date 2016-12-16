# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_work_freelancer_project_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='certification',
            name='title',
            field=models.CharField(max_length=255, default='None'),
        ),
        migrations.AddField(
            model_name='patent',
            name='title',
            field=models.CharField(max_length=255, default='None'),
        ),
        migrations.AddField(
            model_name='publication',
            name='title',
            field=models.CharField(max_length=255, default='None'),
        ),
        migrations.AddField(
            model_name='work',
            name='freelancer_project_details',
            field=models.CharField(max_length=1000, default='None'),
        ),
        migrations.AddField(
            model_name='work',
            name='intership_roles_responsibilities',
            field=models.CharField(max_length=1000, default='None'),
        ),
        migrations.AddField(
            model_name='work',
            name='job_roles_and_responsibilities',
            field=models.CharField(max_length=1000, default='None'),
        ),
    ]
