from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class user_details(models.Model):
	user_id = models.ForeignKey(User)
	short_bio = models.CharField(max_length=1000)
	twitter_handle = models.CharField(max_length=255)
	facebook_url = models.CharField(max_length=255)
	linkedin_url = models.CharField(max_length=255)
	googleplus_url = models.CharField(max_length=255)
	first_name = models.CharField(max_length=255, default="None")
	last_name = models.CharField(max_length=255, default="None")
	profession = models.CharField(max_length=255, default='None')
	dob = models.DateField(null=True, blank=True)
	city = models.CharField(max_length=255)
	photo = models.FileField(upload_to = settings.BASE_DIR + '/media/profile_pic/')
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)

class education(models.Model):
	# def education_filename(instance, filename):
	# 	curr_username = instance.user_id.username
	# 	fname, dot, extension = filename.rpartition('.')
	# 	final_file_name = '%s.%s' % ('education_file', extension)
	# 	path = os.path.join(settings.BASE_DIR, '/media/'+ curr_username + '/', final_file_name)
	# 	try:
	# 		os.makedirs(path)
	# 	except OSError as e:
	# 		if e.errno == 17:
	# 			#Dir already exists
	# 			pass
	# 	return path  
	user_id = models.ForeignKey(User)
	year = models.CharField(max_length=4)
	education_type = models.CharField(max_length=255)
	institution_name = models.CharField(max_length=255)
	what_did_you_do_there = models.CharField(max_length=1000)
	aggregate = models.CharField(max_length=255)
	document = models.FileField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)

class work(models.Model):
	user_id = models.ForeignKey(User)
	work_type = models.CharField(max_length=255)
	internship_company_name = models.CharField(max_length=255)
	internship_date_from = models.DateField(null=True, blank=True)
	internship_date_to = models.DateField(null=True, blank=True)
	internship_title = models.CharField(max_length=255)
	internship_status = models.CharField(max_length=255)
	internship_document = models.FileField(upload_to = settings.BASE_DIR + '/media/work/internship/')
	job_date_from = models.DateField(null=True, blank=True)
	job_date_to = models.DateField(null=True, blank=True)
	job_company_name = models.CharField(max_length=255)
	job_designation = models.CharField(max_length=255)
	job_document = models.FileField(upload_to = settings.BASE_DIR + '/media/work/job/')
	freelancer_client_name = models.CharField(max_length=255)
	freelancer_project_title = models.CharField(max_length=255)
	freelancer_year = models.CharField(max_length=4, default="2016")
	freelancer_link = models.CharField(max_length=255)
	freelancer_status = models.CharField(max_length=255)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)

class certification(models.Model):
	def certification_filename(instance, filename):
		curr_username = instance.user_id.username
		path = settings.BASE_DIR + '/media/certification/' + curr_username
		try:
			os.makedirs(path)
		except OSError as e:
			if e.errno == 17:
				#Dir already exists
				pass
		fname, dot, extension = filename.rpartition('.')
		final_file_name = '%s.%s' % (fname, extension)
		return final_file_name  
	user_id = models.ForeignKey(User)
	year = models.CharField(max_length=4)
	agency = models.CharField(max_length=255)
	mode_of_certification = models.CharField(max_length=255)
	details = models.CharField(max_length=1000)
	document = models.FileField(upload_to = certification_filename)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)

class publication(models.Model):
	user_id = models.ForeignKey(User)
	year = models.CharField(max_length=4)
	mode = models.CharField(max_length=255)
	journal = models.CharField(max_length=1000)
	details = models.CharField(max_length=1000)
	status = models.CharField(max_length=255)
	link = models.CharField(max_length=255)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)

class extracurricular_activities(models.Model):
	user_id = models.ForeignKey(User)
	year = models.CharField(max_length=4)
	activity_type = models.CharField(max_length=255)
	activity_details = models.CharField(max_length=1000, default='none')
	title = models.CharField(max_length=255)
	organization = models.CharField(max_length=255)
	organization_details = models.CharField(max_length=1000)
	link = models.CharField(max_length=255)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)

class patent(models.Model):
	user_id = models.ForeignKey(User)
	year = models.CharField(max_length=4)
	mode = models.CharField(max_length=255)
	patent_details = models.CharField(max_length=255)
	patent_status = models.CharField(max_length=255)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)

class achievements(models.Model):
	def achievements_filename(instance, filename):
		curr_username = instance.user_id.username
		path = settings.BASE_DIR + '/media/achievements/' + curr_username
		try:
			os.makedirs(path)
		except OSError as e:
			if e.errno == 17:
				#Dir already exists
				pass
		fname, dot, extension = filename.rpartition('.')
		final_file_name = '%s.%s' % (fname, extension)
		return final_file_name  
	user_id = models.ForeignKey(User)
	year = models.CharField(max_length=4)
	achievement_type = models.CharField(max_length=255)
	title = models.CharField(max_length=255)
	organization = models.CharField(max_length=255)
	details = models.CharField(max_length=1000)
	link = models.CharField(max_length=255)
	document = models.FileField(upload_to = achievements_filename)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)

class skills(models.Model):
	user_id = models.ForeignKey(User)
	skill_name = models.CharField(max_length=1000)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)

class languages(models.Model):
	user_id = models.ForeignKey(User)
	language_name = models.CharField(max_length=255)
	fluency = models.CharField(max_length=255)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
