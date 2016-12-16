# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='achievements',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('year', models.CharField(max_length=4)),
                ('achievement_type', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('organization', models.CharField(max_length=255)),
                ('details', models.CharField(max_length=1000)),
                ('link', models.CharField(max_length=255)),
                ('document', models.FilePathField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('user_id', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='certification',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('year', models.CharField(max_length=4)),
                ('agency', models.CharField(max_length=255)),
                ('mode_of_certification', models.CharField(max_length=255)),
                ('details', models.CharField(max_length=1000)),
                ('document', models.FilePathField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('user_id', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='education',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('year', models.CharField(max_length=4)),
                ('education_type', models.CharField(max_length=255)),
                ('institution_name', models.CharField(max_length=255)),
                ('what_did_you_do_there', models.CharField(max_length=1000)),
                ('aggregate', models.IntegerField()),
                ('document', models.FilePathField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('user_id', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='extracurricular_activities',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('year', models.CharField(max_length=4)),
                ('activity_type', models.CharField(max_length=255)),
                ('activity_details', models.CharField(max_length=1000, default='none')),
                ('title', models.CharField(max_length=255)),
                ('organization', models.CharField(max_length=255)),
                ('organization_details', models.CharField(max_length=1000)),
                ('link', models.CharField(max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('user_id', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='languages',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('language_name', models.CharField(max_length=255)),
                ('fluency', models.CharField(max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('user_id', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='patent',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('year', models.CharField(max_length=4)),
                ('mode', models.CharField(max_length=255)),
                ('patent_details', models.CharField(max_length=255)),
                ('patent_status', models.CharField(max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('user_id', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='publication',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('year', models.CharField(max_length=4)),
                ('mode', models.CharField(max_length=255)),
                ('journal', models.CharField(max_length=1000)),
                ('details', models.CharField(max_length=1000)),
                ('status', models.CharField(max_length=255)),
                ('link', models.CharField(max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('user_id', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='skills',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('technical_skills', models.CharField(max_length=1000)),
                ('soft_skills', models.CharField(max_length=1000)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('user_id', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='user_details',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('short_bio', models.CharField(max_length=1000)),
                ('twitter_handle', models.CharField(max_length=255)),
                ('facebook_url', models.CharField(max_length=255)),
                ('linkedin_url', models.CharField(max_length=255)),
                ('googleplus_url', models.CharField(max_length=255)),
                ('dob', models.DateField()),
                ('city', models.CharField(max_length=255)),
                ('photo', models.FilePathField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('user_id', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='work',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('work_type', models.CharField(max_length=255)),
                ('internship_company_name', models.CharField(max_length=255)),
                ('internship_date_from', models.DateField()),
                ('internship_date_to', models.DateField()),
                ('internship_title', models.CharField(max_length=255)),
                ('internship_status', models.CharField(max_length=255)),
                ('internship_document', models.FilePathField()),
                ('job_date_from', models.DateField()),
                ('job_date_to', models.DateField()),
                ('job_company_name', models.CharField(max_length=255)),
                ('job_designation', models.CharField(max_length=255)),
                ('job_document', models.FilePathField()),
                ('freelancer_client_name', models.CharField(max_length=255)),
                ('freelancer_project_title', models.CharField(max_length=255)),
                ('freelancer_link', models.CharField(max_length=255)),
                ('freelancer_status', models.CharField(max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('user_id', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
