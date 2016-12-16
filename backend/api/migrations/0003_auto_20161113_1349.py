# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20161110_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achievements',
            name='document',
            field=models.FileField(upload_to='D:\\backend_api\\backend/media/achievements/'),
        ),
        migrations.AlterField(
            model_name='certification',
            name='document',
            field=models.FileField(upload_to='D:\\backend_api\\backend/media/certification/'),
        ),
        migrations.AlterField(
            model_name='education',
            name='document',
            field=models.FileField(upload_to='D:\\backend_api\\backend/media/education/'),
        ),
        migrations.AlterField(
            model_name='user_details',
            name='photo',
            field=models.FileField(upload_to='D:\\backend_api\\backend/media/profile_pic/'),
        ),
        migrations.AlterField(
            model_name='work',
            name='internship_document',
            field=models.FileField(upload_to='D:\\backend_api\\backend/media/internship/'),
        ),
        migrations.AlterField(
            model_name='work',
            name='job_document',
            field=models.FileField(upload_to='D:\\backend_api\\backend/media/job/'),
        ),
    ]
