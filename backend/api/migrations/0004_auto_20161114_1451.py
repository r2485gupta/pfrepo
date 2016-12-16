# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import api.models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20161113_1349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achievements',
            name='document',
            field=models.FileField(upload_to=api.models.achievements.achievements_filename),
        ),
        migrations.AlterField(
            model_name='certification',
            name='document',
            field=models.FileField(upload_to=api.models.certification.certification_filename),
        ),
        migrations.AlterField(
            model_name='education',
            name='document',
            field=models.FileField(),
        ),
        migrations.AlterField(
            model_name='work',
            name='internship_document',
            field=models.FileField(upload_to='D:\\backend_api\\backend/media/work/internship/'),
        ),
        migrations.AlterField(
            model_name='work',
            name='job_document',
            field=models.FileField(upload_to='D:\\backend_api\\backend/media/work/job/'),
        ),
    ]
