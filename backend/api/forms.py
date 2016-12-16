from django import forms
from api.models import *

class loginForm(forms.Form):
	email = forms.CharField(
		label = 'email',
		widget = forms.EmailInput(attrs={'placeholder': 'Email...', 'class': 'form-control'})
	)

	password = forms.CharField(
		label = 'password',
		widget = forms.PasswordInput(attrs={'placeholder': 'Password...', 'class': 'form-control'})
	)

	remember_me = forms.BooleanField(
		required = False,
		initial = True,
		label = 'remember_me',
		widget = forms.CheckboxInput(attrs={'name': 'optionsCheckboxes'})
	)

class signupForm(forms.Form):
	user_name = forms.CharField(
		label = 'user_name',
		widget = forms.TextInput(attrs={'placeholder': 'Username...', 'class': 'form-control'})
	)

	email = forms.CharField(
		label = 'email',
		widget = forms.EmailInput(attrs={'placeholder': 'Email...', 'class': 'form-control'})
	)

	password = forms.CharField(
		label = 'password',
		widget = forms.PasswordInput(attrs={'placeholder': 'Password...', 'class': 'form-control'})
	)

class profile_workForm(forms.Form):
	WORK_TYPE_CHOICES = (
		('Internship', 'Internship'),
		('Job', 'Job'),
		('Freelancer', 'Freelancer')
	)

	PROJECT_STATUS_CHOICES = (
		('Ongoing', 'Ongoing'),
		('Completed', 'Completed')
	)

	work_type = forms.ChoiceField(
		label = 'work_type',
		choices = WORK_TYPE_CHOICES,
		widget = forms.Select(attrs={'class': 'form-control dropdown-toggle', 'id': 'user'})
	)

	internship_company_name = forms.CharField(
		required = False,
		label = 'company_name',
		widget = forms.TextInput(attrs={'class': 'form-control input1', 'name': 'input1'})
	)

	job_company_name = forms.CharField(
		required = False,
		label = 'company_name',
		widget = forms.TextInput(attrs={'class': 'form-control input1', 'name': 'input1'})
	)

	job_designation = forms.CharField(
		required = False,
		label = 'designation',
		widget = forms.TextInput(attrs={'class': 'form-control input1', 'name': 'designation'})
	)

	freelancer_client = forms.CharField(
		required = False,
		label = 'client',
		widget = forms.TextInput(attrs={'class': 'form-control input2', 'name': 'input2'})
	)		

	internship_from_date = forms.CharField(
		required = False,
		label = 'form_date',
		widget = forms.TextInput(attrs={'placeholder': 'dd/mm/yyyy', 'class': 'form-control datepicker'})
	)

	internship_to_date = forms.CharField(
		required = False,
		label = 'to_date',
		widget = forms.TextInput(attrs={'placeholder': 'dd/mm/yyyy', 'class': 'form-control datepicker'})
	)

	job_from_date = forms.CharField(
		required = False,
		label = 'form_date',
		widget = forms.TextInput(attrs={'placeholder': 'dd/mm/yyyy', 'class': 'form-control datepicker'})
	)

	job_to_date = forms.CharField(
		required = False,
		label = 'to_date',
		widget = forms.TextInput(attrs={'placeholder': 'dd/mm/yyyy', 'class': 'form-control datepicker'})
	)

	freelancer_project_title = forms.CharField(
		required = False,
		label = 'freelancer_project_title',
		widget = forms.TextInput(attrs={'class': 'form-control input2', 'name': 'designation'})
	)

	freelancer_link = forms.CharField(
		required = False,
		label = 'link',
		widget = forms.TextInput(attrs={'class': 'form-control input2', 'name': 'designation'})
	)

	freelancer_project_status = forms.ChoiceField(
		required = False,
		label = 'project_status',
		choices = PROJECT_STATUS_CHOICES,
		widget = forms.Select(attrs={'class': 'form-control dropdown-toggle'})
	)

	internship_title = forms.CharField(
		required = False,
		label = 'title',
		widget = forms.TextInput(attrs={'class': 'form-control input2', 'name': 'input2'})
	)

class profile_educationForm(forms.Form):
	PROFILE_EDUCATION_YEAR_CHOICES = (
		('1970', '1970'),
		('1971', '1971'),
		('1972', '1972'),
		('1973', '1973'),
		('1974', '1974'),
		('1975', '1975'),
		('1976', '1976'),
		('1977', '1977'),
		('1978', '1978'),
		('1979', '1979'),
		('1980', '1980'),
		('1981', '1981'),
		('1982', '1982'),
		('1983', '1983'),
		('1984', '1984'),
		('1985', '1985'),
		('1986', '1986'),
		('1987', '1987'),
		('1988', '1988'),
		('1989', '1989'),
		('1990', '1990'),
		('1991', '1991'),
		('1992', '1992'),
		('1993', '1993'),
		('1994', '1994'),
		('1995', '1995'),
		('1996', '1996'),
		('1997', '1997'),
		('1998', '1998'),
		('1999', '1999'),
		('2000', '2000'),
		('2001', '2001'),
		('2002', '2002'),
		('2003', '2003'),
		('2004', '2004'),
		('2005', '2005'),
		('2006', '2006'),
		('2007', '2007'),
		('2008', '2008'),
		('2009', '2009'),
		('2010', '2010'),
		('2011', '2011'),
		('2012', '2012'),
		('2013', '2013'),
		('2014', '2014'),
		('2015', '2015'),
		('2016', '2016'),
	)

	EDUCATION_TYPE_CHOICES = (
		('High School', 'High School'),
		('Intermediate', 'Intermediate'),
		('Bachelors', 'Bachelors'),
		('Masters', 'Masters'),
		('Post Graduation', 'Post Graduation')
	)

	year = forms.ChoiceField(
		label = 'year',
		required = False,
		choices = PROFILE_EDUCATION_YEAR_CHOICES,
		widget = forms.Select(attrs={'class': 'form-control dropdown-toggle'})
	)

	education_type = forms.ChoiceField(
		label = 'year',
		required = False,
		choices = EDUCATION_TYPE_CHOICES,
		widget = forms.Select(attrs={'class': 'form-control dropdown-toggle'})
	)

	institution = forms.CharField(
		label = 'institution',
		required = False,
		widget = forms.TextInput(attrs={'class': 'form-control input2'})
	)

	aggregate = forms.CharField(
		label = 'aggregate',
		required = False,
		widget = forms.TextInput(attrs={'class': 'form-control'})
	)

	what_did_you_do_there = forms.CharField(
		label = 'what_did_you_do_there',
		required = False,
		widget = forms.Textarea(attrs={'placeholder': 'What did you do there?', 'class': 'form-control', 'rows': '5'})
	)

	# attach_file = forms.FileField(
	# 	label = 'attach a file'
	# )

class profile_certificationForm(forms.Form):
	CERTIFICATION_MODE_CHOICES = (
		('Online', 'Online'),
		('Offline', 'Offline')
	)

	PROFILE_CERTIFICATION_YEAR_CHOICES = (
		('1970', '1970'),
		('1971', '1971'),
		('1972', '1972'),
		('1973', '1973'),
		('1974', '1974'),
		('1975', '1975'),
		('1976', '1976'),
		('1977', '1977'),
		('1978', '1978'),
		('1979', '1979'),
		('1980', '1980'),
		('1981', '1981'),
		('1982', '1982'),
		('1983', '1983'),
		('1984', '1984'),
		('1985', '1985'),
		('1986', '1986'),
		('1987', '1987'),
		('1988', '1988'),
		('1989', '1989'),
		('1990', '1990'),
		('1991', '1991'),
		('1992', '1992'),
		('1993', '1993'),
		('1994', '1994'),
		('1995', '1995'),
		('1996', '1996'),
		('1997', '1997'),
		('1998', '1998'),
		('1999', '1999'),
		('2000', '2000'),
		('2001', '2001'),
		('2002', '2002'),
		('2003', '2003'),
		('2004', '2004'),
		('2005', '2005'),
		('2006', '2006'),
		('2007', '2007'),
		('2008', '2008'),
		('2009', '2009'),
		('2010', '2010'),
		('2011', '2011'),
		('2012', '2012'),
		('2013', '2013'),
		('2014', '2014'),
		('2015', '2015'),
		('2016', '2016'),
	)

	year = forms.ChoiceField(
		label = 'year',
		choices = PROFILE_CERTIFICATION_YEAR_CHOICES,
		required = False,
		widget = forms.Select(attrs={'class': 'form-control dropdown-toggle'})
	)

	agency = forms.CharField(
		label = 'agency',
		required = False,
		widget = forms.TextInput(attrs={'class': 'form-control input1'})
	)

	mode = forms.ChoiceField(
		label = 'year',
		choices = CERTIFICATION_MODE_CHOICES,
		required = False,
		widget = forms.Select(attrs={'class': 'form-control dropdown-toggle'})
	)

	details = forms.CharField(
		label = 'details',
		required = False,
		widget = forms.Textarea(attrs={'placeholder': 'Details', 'class': 'form-control', 'rows': '5'})
	)

	# attach_file = forms.FileField(
	# 	label = 'attach a file'
	# )

class profile_publicationForm(forms.Form):
	PROFILE_PUBLICATION_YEAR_CHOICES = (
		('1970', '1970'),
		('1971', '1971'),
		('1972', '1972'),
		('1973', '1973'),
		('1974', '1974'),
		('1975', '1975'),
		('1976', '1976'),
		('1977', '1977'),
		('1978', '1978'),
		('1979', '1979'),
		('1980', '1980'),
		('1981', '1981'),
		('1982', '1982'),
		('1983', '1983'),
		('1984', '1984'),
		('1985', '1985'),
		('1986', '1986'),
		('1987', '1987'),
		('1988', '1988'),
		('1989', '1989'),
		('1990', '1990'),
		('1991', '1991'),
		('1992', '1992'),
		('1993', '1993'),
		('1994', '1994'),
		('1995', '1995'),
		('1996', '1996'),
		('1997', '1997'),
		('1998', '1998'),
		('1999', '1999'),
		('2000', '2000'),
		('2001', '2001'),
		('2002', '2002'),
		('2003', '2003'),
		('2004', '2004'),
		('2005', '2005'),
		('2006', '2006'),
		('2007', '2007'),
		('2008', '2008'),
		('2009', '2009'),
		('2010', '2010'),
		('2011', '2011'),
		('2012', '2012'),
		('2013', '2013'),
		('2014', '2014'),
		('2015', '2015'),
		('2016', '2016'),
	)

	PUBLICATION_MODE_CHOICES = (
		('National', 'National'),
		('International', 'International')
	)

	PUBLICATION_STATUS_CHOICES = (
		('Manuscript Under Preparation', 'Manuscript Under Preparation'),
		('Submitted', 'Submitted'),
		('Communicated', 'Communicated')
	)

	year = forms.ChoiceField(
		label = 'year',
		required = False,
		choices = PROFILE_PUBLICATION_YEAR_CHOICES,
		widget = forms.Select(attrs={'class': 'form-control dropdown-toggle'})
	)

	mode = forms.ChoiceField(
		label = 'mode',
		required = False,
		choices = PUBLICATION_MODE_CHOICES,
		widget = forms.Select(attrs={'class': 'form-control dropdown-toggle'})
	)

	journal = forms.CharField(
		label = 'journal',
		required = False,
		widget = forms.TextInput(attrs={'class': 'form-control'})
	)

	details = forms.CharField(
		label = 'details',
		required = False,
		widget = forms.Textarea(attrs={'placeholder': 'Details', 'class': 'form-control', 'rows': '5'})
	)

	status = forms.ChoiceField(
		label = 'status',
		required = False,
		choices = PUBLICATION_STATUS_CHOICES,
		widget = forms.Select(attrs={'placeholder': 'Status', 'class': 'form-control dropdown-toggle'})
	)

	link = forms.CharField(
		label = 'link',
		required = False,
		widget = forms.TextInput(attrs={'class': 'form-control input2', 'name': 'input2'})
	)

class profile_extracurricularForm(forms.Form):
	PROFILE_EXTRACURRICULAR_YEAR_CHOICES = (
		('1970', '1970'),
		('1971', '1971'),
		('1972', '1972'),
		('1973', '1973'),
		('1974', '1974'),
		('1975', '1975'),
		('1976', '1976'),
		('1977', '1977'),
		('1978', '1978'),
		('1979', '1979'),
		('1980', '1980'),
		('1981', '1981'),
		('1982', '1982'),
		('1983', '1983'),
		('1984', '1984'),
		('1985', '1985'),
		('1986', '1986'),
		('1987', '1987'),
		('1988', '1988'),
		('1989', '1989'),
		('1990', '1990'),
		('1991', '1991'),
		('1992', '1992'),
		('1993', '1993'),
		('1994', '1994'),
		('1995', '1995'),
		('1996', '1996'),
		('1997', '1997'),
		('1998', '1998'),
		('1999', '1999'),
		('2000', '2000'),
		('2001', '2001'),
		('2002', '2002'),
		('2003', '2003'),
		('2004', '2004'),
		('2005', '2005'),
		('2006', '2006'),
		('2007', '2007'),
		('2008', '2008'),
		('2009', '2009'),
		('2010', '2010'),
		('2011', '2011'),
		('2012', '2012'),
		('2013', '2013'),
		('2014', '2014'),
		('2015', '2015'),
		('2016', '2016'),
	)

	PROFILE_EXTRACURRICULAR_TYPE_CHOICES = (
		('Volunteer Activity', 'Volunteer Activity'),
		('Event Organizing', 'Event Organizing'),
		('Other', 'Other')
	)

	year = forms.ChoiceField(
		label = 'year',
		required = False,
		choices = PROFILE_EXTRACURRICULAR_YEAR_CHOICES,
		widget = forms.Select(attrs={'class': 'form-control dropdown-toggle'})
	)

	activity_type = forms.ChoiceField(
		label = 'activity type',
		required = False,
		choices = PROFILE_EXTRACURRICULAR_TYPE_CHOICES,
		widget = forms.Select(attrs={'class': 'form-control dropdown-toggle'})
	)	

	title = forms.CharField(
		label = 'title',
		required = False,
		widget = forms.TextInput(attrs={'class': 'form-control'})
	)

	details = forms.CharField(
		label = 'details',
		required = False,
		widget = forms.Textarea(attrs={'placeholder': 'Details', 'class': 'form-control', 'rows': '5'})
	)

	organization = forms.CharField(
		label = 'organization',
		required = False,
		widget = forms.TextInput(attrs={'class': 'form-control'})
	)

	link = forms.CharField(
		label = 'link',
		required = False,
		widget = forms.TextInput(attrs={'class': 'form-control'})
	)

class profile_patentForm(forms.Form):
	PROFILE_PUBLICATION_YEAR_CHOICES = (
		('1970', '1970'),
		('1971', '1971'),
		('1972', '1972'),
		('1973', '1973'),
		('1974', '1974'),
		('1975', '1975'),
		('1976', '1976'),
		('1977', '1977'),
		('1978', '1978'),
		('1979', '1979'),
		('1980', '1980'),
		('1981', '1981'),
		('1982', '1982'),
		('1983', '1983'),
		('1984', '1984'),
		('1985', '1985'),
		('1986', '1986'),
		('1987', '1987'),
		('1988', '1988'),
		('1989', '1989'),
		('1990', '1990'),
		('1991', '1991'),
		('1992', '1992'),
		('1993', '1993'),
		('1994', '1994'),
		('1995', '1995'),
		('1996', '1996'),
		('1997', '1997'),
		('1998', '1998'),
		('1999', '1999'),
		('2000', '2000'),
		('2001', '2001'),
		('2002', '2002'),
		('2003', '2003'),
		('2004', '2004'),
		('2005', '2005'),
		('2006', '2006'),
		('2007', '2007'),
		('2008', '2008'),
		('2009', '2009'),
		('2010', '2010'),
		('2011', '2011'),
		('2012', '2012'),
		('2013', '2013'),
		('2014', '2014'),
		('2015', '2015'),
		('2016', '2016'),
	)

	PATENT_MODE_CHOICES = (
		('National', 'National'),
		('International', 'International')
	)

	PATENT_STATUS_CHOICES = (
		('Applied', 'Applied'),
		('Approved', 'Approved')
	)

	year = forms.ChoiceField(
		label = 'year',
		required = False,
		choices = PROFILE_PUBLICATION_YEAR_CHOICES,
		widget = forms.Select(attrs={'class': 'form-control dropdown-toggle'})
	)

	mode = forms.ChoiceField(
		label = 'mode',
		required = False,
		choices = PATENT_MODE_CHOICES,
		widget = forms.Select(attrs={'class': 'form-control dropdown-toggle'})
	)

	status = forms.ChoiceField(
		label = 'status',
		required = False,
		choices = PATENT_STATUS_CHOICES,
		widget = forms.Select(attrs={'class': 'form-control dropdown-toggle'})
	)	

	details = forms.CharField(
		label = 'details',
		required = False,
		widget = forms.Textarea(attrs={'placeholder': 'Details', 'class': 'form-control', 'rows': '5'})
	)

class profile_achievementForm(forms.Form):
	PROFILE_PUBLICATION_YEAR_CHOICES = (
		('1970', '1970'),
		('1971', '1971'),
		('1972', '1972'),
		('1973', '1973'),
		('1974', '1974'),
		('1975', '1975'),
		('1976', '1976'),
		('1977', '1977'),
		('1978', '1978'),
		('1979', '1979'),
		('1980', '1980'),
		('1981', '1981'),
		('1982', '1982'),
		('1983', '1983'),
		('1984', '1984'),
		('1985', '1985'),
		('1986', '1986'),
		('1987', '1987'),
		('1988', '1988'),
		('1989', '1989'),
		('1990', '1990'),
		('1991', '1991'),
		('1992', '1992'),
		('1993', '1993'),
		('1994', '1994'),
		('1995', '1995'),
		('1996', '1996'),
		('1997', '1997'),
		('1998', '1998'),
		('1999', '1999'),
		('2000', '2000'),
		('2001', '2001'),
		('2002', '2002'),
		('2003', '2003'),
		('2004', '2004'),
		('2005', '2005'),
		('2006', '2006'),
		('2007', '2007'),
		('2008', '2008'),
		('2009', '2009'),
		('2010', '2010'),
		('2011', '2011'),
		('2012', '2012'),
		('2013', '2013'),
		('2014', '2014'),
		('2015', '2015'),
		('2016', '2016'),
	)

	ACHIEVEMENT_TYPE_CHOICES = (
		('Award', 'Award'),
		('Scholarship', 'Scholarship')
	)

	year = forms.ChoiceField(
		label = 'year',
		required = False,
		choices = PROFILE_PUBLICATION_YEAR_CHOICES,
		widget = forms.Select(attrs={'class': 'form-control dropdown-toggle'})
	)

	achievement_type = forms.ChoiceField(
		label = 'achievement type',
		required = False,
		choices = ACHIEVEMENT_TYPE_CHOICES,
		widget = forms.Select(attrs={'class': 'form-control dropdown-toggle'})
	)
	
	title = forms.CharField(
		label = 'title',
		required = False,
		widget = forms.TextInput(attrs={'class': 'form-control'})
	)

	organization = forms.CharField(
		label = 'organization',
		required = False,
		widget = forms.TextInput(attrs={'class': 'form-control'})
	)	

	details = forms.CharField(
		label = 'details',
		required = False,
		widget = forms.Textarea(attrs={'placeholder': 'Details', 'class': 'form-control', 'rows': '5'})
	)

	link = forms.CharField(
		label = 'link',
		required = False,
		widget = forms.TextInput(attrs={'class': 'form-control'})
	)

	# attach_file = forms.FileField(
	# 	label = 'attach a file'
	# )

class profile_aboutmeForm(forms.Form):
	first_name = forms.CharField(
		label = 'first name',
		required = False,
		widget = forms.TextInput(attrs={'class': 'form-control input2'})
	)

	last_name = forms.CharField(
		label = 'last name',
		required = False,
		widget = forms.TextInput(attrs={'class': 'form-control input2'})
	)

	profession = forms.CharField(
		label = 'profession',
		required = False,
		widget = forms.TextInput(attrs={'class': 'form-control input2'})
	)

	dob = forms.CharField(		
		label = 'form_date',
		required = False,
		widget = forms.TextInput(attrs={'placeholder': 'dd/mm/yyyy', 'class': 'form-control datepicker'})
	)

	short_bio = forms.CharField(
		label = 'short_bio',
		required = False,
		widget = forms.Textarea(attrs={'placeholder': 'Short Bio', 'class': 'form-control', 'rows': '5'})
	)

	facebook_url = forms.CharField(
		label = 'facebook url',
		required = False,
		widget = forms.TextInput(attrs={'class': 'form-control'})
	)

	twitter_handle = forms.CharField(
		label = 'twitter handle',
		required = False,
		widget = forms.TextInput(attrs={'class': 'form-control'})
	)

	linkedin_url = forms.CharField(
		label = 'linkedin url',
		required = False,
		widget = forms.TextInput(attrs={'class': 'form-control'})
	)

class profile_education_add_editForm(forms.Form):
	PROFILE_EDUCATION_ADD_YEAR_CHOICES = (
		('1970', '1970'),
		('1971', '1971'),
		('1972', '1972'),
		('1973', '1973'),
		('1974', '1974'),
		('1975', '1975'),
		('1976', '1976'),
		('1977', '1977'),
		('1978', '1978'),
		('1979', '1979'),
		('1980', '1980'),
		('1981', '1981'),
		('1982', '1982'),
		('1983', '1983'),
		('1984', '1984'),
		('1985', '1985'),
		('1986', '1986'),
		('1987', '1987'),
		('1988', '1988'),
		('1989', '1989'),
		('1990', '1990'),
		('1991', '1991'),
		('1992', '1992'),
		('1993', '1993'),
		('1994', '1994'),
		('1995', '1995'),
		('1996', '1996'),
		('1997', '1997'),
		('1998', '1998'),
		('1999', '1999'),
		('2000', '2000'),
		('2001', '2001'),
		('2002', '2002'),
		('2003', '2003'),
		('2004', '2004'),
		('2005', '2005'),
		('2006', '2006'),
		('2007', '2007'),
		('2008', '2008'),
		('2009', '2009'),
		('2010', '2010'),
		('2011', '2011'),
		('2012', '2012'),
		('2013', '2013'),
		('2014', '2014'),
		('2015', '2015'),
		('2016', '2016'),
	)

	EDUCATION_ADD_TYPE_CHOICES = (
		('High School', 'High School'),
		('Intermediate', 'Intermediate'),
		('Bachelors', 'Bachelors'),
		('Masters', 'Masters'),
		('Post Graduation', 'Post Graduation')
	)

	tuple_id = forms.CharField(
		required = False,
		label = 'tuple_id',
		widget = forms.TextInput(attrs={'class': 'form-control input2'})
	)

	year = forms.ChoiceField(
		label = 'year',
		required = False,
		choices = PROFILE_EDUCATION_ADD_YEAR_CHOICES,
		widget = forms.Select(attrs={'class': 'form-control dropdown-toggle'})
	)

	education_type = forms.ChoiceField(
		label = 'education_type',
		required = False,
		choices = EDUCATION_ADD_TYPE_CHOICES,
		widget = forms.Select(attrs={'class': 'form-control dropdown-toggle'})
	)

	institution = forms.CharField(
		label = 'institution',
		required = False,
		widget = forms.TextInput(attrs={'class': 'form-control input2'})
	)

	aggregate = forms.CharField(
		label = 'aggregate',
		required = False,
		widget = forms.TextInput(attrs={'class': 'form-control'})
	)

	what_did_you_do_there = forms.CharField(
		label = 'what_did_you_do_there',
		required = False,
		widget = forms.Textarea(attrs={'placeholder': 'What did you do there?', 'class': 'form-control', 'rows': '5'})
	)

	attach_file = forms.FileField(
		required = False,
		label = 'attach a file',
		widget = forms.FileInput(attrs={'class': 'form-control'})
	)

class profile_work_add_editForm(forms.Form):
	PROFILE_WORK_ADD_YEAR_CHOICES = (
		('1970', '1970'),
		('1971', '1971'),
		('1972', '1972'),
		('1973', '1973'),
		('1974', '1974'),
		('1975', '1975'),
		('1976', '1976'),
		('1977', '1977'),
		('1978', '1978'),
		('1979', '1979'),
		('1980', '1980'),
		('1981', '1981'),
		('1982', '1982'),
		('1983', '1983'),
		('1984', '1984'),
		('1985', '1985'),
		('1986', '1986'),
		('1987', '1987'),
		('1988', '1988'),
		('1989', '1989'),
		('1990', '1990'),
		('1991', '1991'),
		('1992', '1992'),
		('1993', '1993'),
		('1994', '1994'),
		('1995', '1995'),
		('1996', '1996'),
		('1997', '1997'),
		('1998', '1998'),
		('1999', '1999'),
		('2000', '2000'),
		('2001', '2001'),
		('2002', '2002'),
		('2003', '2003'),
		('2004', '2004'),
		('2005', '2005'),
		('2006', '2006'),
		('2007', '2007'),
		('2008', '2008'),
		('2009', '2009'),
		('2010', '2010'),
		('2011', '2011'),
		('2012', '2012'),
		('2013', '2013'),
		('2014', '2014'),
		('2015', '2015'),
		('2016', '2016'),
	)

	WORK_TYPE_CHOICES = (
		('Internship', 'Internship'),
		('Job', 'Job'),
		('Freelancer', 'Freelancer')
	)

	PROJECT_STATUS_CHOICES = (
		('Ongoing', 'Ongoing'),
		('Completed', 'Completed')
	)

	tuple_id = forms.CharField(
		required = False,
		label = 'tuple_id',
		widget = forms.TextInput(attrs={'class': 'form-control input2'})
	)

	work_type = forms.ChoiceField(
		label = 'work_type',
		required = False,
		choices = WORK_TYPE_CHOICES,
		widget = forms.Select(attrs={'class': 'form-control dropdown-toggle', 'id': 'user_p'})
	)

	internship_company_name = forms.CharField(
		required = False,
		label = 'company_name',
		widget = forms.TextInput(attrs={'class': 'form-control input1', 'name': 'input1'})
	)

	job_company_name = forms.CharField(
		required = False,
		label = 'company_name',
		widget = forms.TextInput(attrs={'class': 'form-control input1', 'name': 'input1'})
	)

	job_designation = forms.CharField(
		required = False,
		label = 'designation',
		widget = forms.TextInput(attrs={'class': 'form-control input1', 'name': 'designation'})
	)

	freelancer_client = forms.CharField(
		required = False,
		label = 'client',
		widget = forms.TextInput(attrs={'class': 'form-control input2', 'name': 'input2'})
	)		

	internship_from_date = forms.CharField(
		required = False,
		label = 'form_date',
		widget = forms.TextInput(attrs={'placeholder': 'dd/mm/yyyy', 'class': 'form-control datepicker'})
	)

	internship_to_date = forms.CharField(
		required = False,
		label = 'to_date',
		widget = forms.TextInput(attrs={'placeholder': 'dd/mm/yyyy', 'class': 'form-control datepicker'})
	)

	job_from_date = forms.CharField(
		required = False,
		label = 'form_date',
		widget = forms.TextInput(attrs={'placeholder': 'dd/mm/yyyy', 'class': 'form-control datepicker'})
	)

	job_to_date = forms.CharField(
		required = False,
		label = 'to_date',
		widget = forms.TextInput(attrs={'placeholder': 'dd/mm/yyyy', 'class': 'form-control datepicker'})
	)

	freelancer_project_title = forms.CharField(
		required = False,
		label = 'freelancer_project_title',
		widget = forms.TextInput(attrs={'class': 'form-control input2', 'name': 'designation'})
	)

	freelancer_link = forms.CharField(
		required = False,
		label = 'link',
		widget = forms.TextInput(attrs={'class': 'form-control input2', 'name': 'designation'})
	)

	freelancer_project_status = forms.ChoiceField(
		required = False,
		label = 'project_status',
		choices = PROJECT_STATUS_CHOICES,
		widget = forms.Select(attrs={'class': 'form-control dropdown-toggle'})
	)

	internship_title = forms.CharField(
		required = False,
		label = 'title',
		widget = forms.TextInput(attrs={'class': 'form-control input2', 'name': 'input2'})
	)

	freelancer_year = forms.ChoiceField(
		required = False,
		label = 'Freelancer Project Year',
		choices = PROFILE_WORK_ADD_YEAR_CHOICES,
		widget = forms.Select(attrs={'class': 'form-control dropdown-toggle'})
	)

class profile_certification_add_editForm(forms.Form):
	PROFILE_CERTIFICATION_YEAR_CHOICES = (
		('1970', '1970'),
		('1971', '1971'),
		('1972', '1972'),
		('1973', '1973'),
		('1974', '1974'),
		('1975', '1975'),
		('1976', '1976'),
		('1977', '1977'),
		('1978', '1978'),
		('1979', '1979'),
		('1980', '1980'),
		('1981', '1981'),
		('1982', '1982'),
		('1983', '1983'),
		('1984', '1984'),
		('1985', '1985'),
		('1986', '1986'),
		('1987', '1987'),
		('1988', '1988'),
		('1989', '1989'),
		('1990', '1990'),
		('1991', '1991'),
		('1992', '1992'),
		('1993', '1993'),
		('1994', '1994'),
		('1995', '1995'),
		('1996', '1996'),
		('1997', '1997'),
		('1998', '1998'),
		('1999', '1999'),
		('2000', '2000'),
		('2001', '2001'),
		('2002', '2002'),
		('2003', '2003'),
		('2004', '2004'),
		('2005', '2005'),
		('2006', '2006'),
		('2007', '2007'),
		('2008', '2008'),
		('2009', '2009'),
		('2010', '2010'),
		('2011', '2011'),
		('2012', '2012'),
		('2013', '2013'),
		('2014', '2014'),
		('2015', '2015'),
		('2016', '2016'),
	)

	CERTIFICATION_MODE_CHOICES = (
		('Online', 'Online'),
		('Offline', 'Offline')
	)

	tuple_id = forms.CharField(
		required = False,
		label = 'tuple_id',
		widget = forms.TextInput(attrs={'class': 'form-control input2'})
	)

	year = forms.ChoiceField(
		label = 'year',
		required = False,
		choices = PROFILE_CERTIFICATION_YEAR_CHOICES,
		widget = forms.Select(attrs={'class': 'form-control dropdown-toggle'})
	)

	agency = forms.CharField(
		label = 'agency',
		required = False,
		widget = forms.TextInput(attrs={'class': 'form-control input1'})
	)

	mode = forms.ChoiceField(
		label = 'mode',
		required = False,
		choices = CERTIFICATION_MODE_CHOICES,
		widget = forms.Select(attrs={'class': 'form-control dropdown-toggle'})
	)

	details = forms.CharField(
		label = 'details',
		required = False,
		widget = forms.Textarea(attrs={'placeholder': 'Details', 'class': 'form-control', 'rows': '5'})
	)

	# attach_file = forms.FileField(
	# 	label = 'attach a file'
	# )	

class profile_skills_add_editForm(forms.Form):
	skill = forms.CharField(
		label = 'skills',
		required = False,
		widget = forms.TextInput(attrs={'class': 'tags', 'id': 'tags_1'})
	)

class profile_extracurricular_add_editForm(forms.Form):
	PROFILE_EXTRACURRICULAR_YEAR_CHOICES = (
		('1970', '1970'),
		('1971', '1971'),
		('1972', '1972'),
		('1973', '1973'),
		('1974', '1974'),
		('1975', '1975'),
		('1976', '1976'),
		('1977', '1977'),
		('1978', '1978'),
		('1979', '1979'),
		('1980', '1980'),
		('1981', '1981'),
		('1982', '1982'),
		('1983', '1983'),
		('1984', '1984'),
		('1985', '1985'),
		('1986', '1986'),
		('1987', '1987'),
		('1988', '1988'),
		('1989', '1989'),
		('1990', '1990'),
		('1991', '1991'),
		('1992', '1992'),
		('1993', '1993'),
		('1994', '1994'),
		('1995', '1995'),
		('1996', '1996'),
		('1997', '1997'),
		('1998', '1998'),
		('1999', '1999'),
		('2000', '2000'),
		('2001', '2001'),
		('2002', '2002'),
		('2003', '2003'),
		('2004', '2004'),
		('2005', '2005'),
		('2006', '2006'),
		('2007', '2007'),
		('2008', '2008'),
		('2009', '2009'),
		('2010', '2010'),
		('2011', '2011'),
		('2012', '2012'),
		('2013', '2013'),
		('2014', '2014'),
		('2015', '2015'),
		('2016', '2016'),
	)

	PROFILE_EXTRACURRICULAR_TYPE_CHOICES = (
		('Volunteer Activity', 'Volunteer Activity'),
		('Event Organizing', 'Event Organizing'),
		('Other', 'Other')
	)

	tuple_id = forms.CharField(
		required = False,
		label = 'tuple_id',
		widget = forms.TextInput(attrs={'class': 'form-control input2'})
	)

	year = forms.ChoiceField(
		label = 'year',
		required = False,
		choices = PROFILE_EXTRACURRICULAR_YEAR_CHOICES,
		widget = forms.Select(attrs={'class': 'form-control dropdown-toggle'})
	)

	activity_type = forms.ChoiceField(
		label = 'activity type',
		required = False,
		choices = PROFILE_EXTRACURRICULAR_TYPE_CHOICES,
		widget = forms.Select(attrs={'class': 'form-control dropdown-toggle'})
	)	

	title = forms.CharField(
		label = 'title',
		required = False,
		widget = forms.TextInput(attrs={'class': 'form-control'})
	)

	details = forms.CharField(
		label = 'details',
		required = False,
		widget = forms.Textarea(attrs={'placeholder': 'Details', 'class': 'form-control', 'rows': '5'})
	)

	organization = forms.CharField(
		label = 'organization',
		required = False,
		widget = forms.TextInput(attrs={'class': 'form-control'})
	)

	link = forms.CharField(
		label = 'link',
		required = False,
		widget = forms.TextInput(attrs={'class': 'form-control'})
	)

class profile_achievements_add_editForm(forms.Form):
	PROFILE_PUBLICATION_YEAR_CHOICES = (
		('1970', '1970'),
		('1971', '1971'),
		('1972', '1972'),
		('1973', '1973'),
		('1974', '1974'),
		('1975', '1975'),
		('1976', '1976'),
		('1977', '1977'),
		('1978', '1978'),
		('1979', '1979'),
		('1980', '1980'),
		('1981', '1981'),
		('1982', '1982'),
		('1983', '1983'),
		('1984', '1984'),
		('1985', '1985'),
		('1986', '1986'),
		('1987', '1987'),
		('1988', '1988'),
		('1989', '1989'),
		('1990', '1990'),
		('1991', '1991'),
		('1992', '1992'),
		('1993', '1993'),
		('1994', '1994'),
		('1995', '1995'),
		('1996', '1996'),
		('1997', '1997'),
		('1998', '1998'),
		('1999', '1999'),
		('2000', '2000'),
		('2001', '2001'),
		('2002', '2002'),
		('2003', '2003'),
		('2004', '2004'),
		('2005', '2005'),
		('2006', '2006'),
		('2007', '2007'),
		('2008', '2008'),
		('2009', '2009'),
		('2010', '2010'),
		('2011', '2011'),
		('2012', '2012'),
		('2013', '2013'),
		('2014', '2014'),
		('2015', '2015'),
		('2016', '2016'),
	)

	ACHIEVEMENT_TYPE_CHOICES = (
		('Award', 'Award'),
		('Scholarship', 'Scholarship')
	)

	tuple_id = forms.CharField(
		required = False,
		label = 'tuple_id',
		widget = forms.TextInput(attrs={'class': 'form-control input2'})
	)

	year = forms.ChoiceField(
		label = 'year',
		required = False,
		choices = PROFILE_PUBLICATION_YEAR_CHOICES,
		widget = forms.Select(attrs={'class': 'form-control dropdown-toggle'})
	)

	achievement_type = forms.ChoiceField(
		label = 'achievement type',
		required = False,
		choices = ACHIEVEMENT_TYPE_CHOICES,
		widget = forms.Select(attrs={'class': 'form-control dropdown-toggle'})
	)
	
	title = forms.CharField(
		label = 'title',
		required = False,
		widget = forms.TextInput(attrs={'class': 'form-control'})
	)

	organization = forms.CharField(
		label = 'organization',
		required = False,
		widget = forms.TextInput(attrs={'class': 'form-control'})
	)	

	details = forms.CharField(
		label = 'details',
		required = False,
		widget = forms.Textarea(attrs={'placeholder': 'Details', 'class': 'form-control', 'rows': '5'})
	)

	link = forms.CharField(
		label = 'link',
		required = False,
		widget = forms.TextInput(attrs={'class': 'form-control'})
	)

	# attach_file = forms.FileField(
	# 	label = 'attach a file'
	# )

class profile_publications_add_editForm(forms.Form):
	PROFILE_PUBLICATION_YEAR_CHOICES = (
		('1970', '1970'),
		('1971', '1971'),
		('1972', '1972'),
		('1973', '1973'),
		('1974', '1974'),
		('1975', '1975'),
		('1976', '1976'),
		('1977', '1977'),
		('1978', '1978'),
		('1979', '1979'),
		('1980', '1980'),
		('1981', '1981'),
		('1982', '1982'),
		('1983', '1983'),
		('1984', '1984'),
		('1985', '1985'),
		('1986', '1986'),
		('1987', '1987'),
		('1988', '1988'),
		('1989', '1989'),
		('1990', '1990'),
		('1991', '1991'),
		('1992', '1992'),
		('1993', '1993'),
		('1994', '1994'),
		('1995', '1995'),
		('1996', '1996'),
		('1997', '1997'),
		('1998', '1998'),
		('1999', '1999'),
		('2000', '2000'),
		('2001', '2001'),
		('2002', '2002'),
		('2003', '2003'),
		('2004', '2004'),
		('2005', '2005'),
		('2006', '2006'),
		('2007', '2007'),
		('2008', '2008'),
		('2009', '2009'),
		('2010', '2010'),
		('2011', '2011'),
		('2012', '2012'),
		('2013', '2013'),
		('2014', '2014'),
		('2015', '2015'),
		('2016', '2016'),
	)

	PUBLICATION_MODE_CHOICES = (
		('National', 'National'),
		('International', 'International')
	)

	PUBLICATION_STATUS_CHOICES = (
		('Manuscript Under Preparation', 'Manuscript Under Preparation'),
		('Submitted', 'Submitted'),
		('Communicated', 'Communicated')
	)

	tuple_id = forms.CharField(
		required = False,
		label = 'tuple_id',
		widget = forms.TextInput(attrs={'class': 'form-control input2'})
	)

	year = forms.ChoiceField(
		label = 'year',
		required = False,
		choices = PROFILE_PUBLICATION_YEAR_CHOICES,
		widget = forms.Select(attrs={'class': 'form-control dropdown-toggle'})
	)

	mode = forms.ChoiceField(
		label = 'mode',
		required = False,
		choices = PUBLICATION_MODE_CHOICES,
		widget = forms.Select(attrs={'class': 'form-control dropdown-toggle'})
	)

	journal = forms.CharField(
		label = 'journal',
		required = False,
		widget = forms.TextInput(attrs={'class': 'form-control'})
	)

	details = forms.CharField(
		label = 'details',
		required = False,
		widget = forms.Textarea(attrs={'placeholder': 'Details', 'class': 'form-control', 'rows': '5'})
	)

	status = forms.ChoiceField(
		label = 'status',
		choices = PUBLICATION_STATUS_CHOICES,
		required = False,
		widget = forms.Select(attrs={'placeholder': 'Status', 'class': 'form-control dropdown-toggle'})
	)

	link = forms.CharField(
		label = 'link',
		required = False,
		widget = forms.TextInput(attrs={'class': 'form-control input2', 'name': 'input2'})
	)


class profile_patent_add_editForm(forms.Form):
	PROFILE_PUBLICATION_YEAR_CHOICES = (
		('1970', '1970'),
		('1971', '1971'),
		('1972', '1972'),
		('1973', '1973'),
		('1974', '1974'),
		('1975', '1975'),
		('1976', '1976'),
		('1977', '1977'),
		('1978', '1978'),
		('1979', '1979'),
		('1980', '1980'),
		('1981', '1981'),
		('1982', '1982'),
		('1983', '1983'),
		('1984', '1984'),
		('1985', '1985'),
		('1986', '1986'),
		('1987', '1987'),
		('1988', '1988'),
		('1989', '1989'),
		('1990', '1990'),
		('1991', '1991'),
		('1992', '1992'),
		('1993', '1993'),
		('1994', '1994'),
		('1995', '1995'),
		('1996', '1996'),
		('1997', '1997'),
		('1998', '1998'),
		('1999', '1999'),
		('2000', '2000'),
		('2001', '2001'),
		('2002', '2002'),
		('2003', '2003'),
		('2004', '2004'),
		('2005', '2005'),
		('2006', '2006'),
		('2007', '2007'),
		('2008', '2008'),
		('2009', '2009'),
		('2010', '2010'),
		('2011', '2011'),
		('2012', '2012'),
		('2013', '2013'),
		('2014', '2014'),
		('2015', '2015'),
		('2016', '2016'),
	)

	PATENT_MODE_CHOICES = (
		('National', 'National'),
		('International', 'International')
	)

	PATENT_STATUS_CHOICES = (
		('Applied', 'Applied'),
		('Approved', 'Approved')
	)

	tuple_id = forms.CharField(
		required = False,
		label = 'tuple_id',
		widget = forms.TextInput(attrs={'class': 'form-control input2'})
	)

	year = forms.ChoiceField(
		label = 'year',
		required = False,
		choices = PROFILE_PUBLICATION_YEAR_CHOICES,
		widget = forms.Select(attrs={'class': 'form-control dropdown-toggle'})
	)

	mode = forms.ChoiceField(
		label = 'mode',
		required = False,
		choices = PATENT_MODE_CHOICES,
		widget = forms.Select(attrs={'class': 'form-control dropdown-toggle'})
	)

	status = forms.ChoiceField(
		label = 'status',
		required = False,
		choices = PATENT_STATUS_CHOICES,
		widget = forms.Select(attrs={'class': 'form-control dropdown-toggle'})
	)	

	details = forms.CharField(
		label = 'details',
		required = False,
		widget = forms.Textarea(attrs={'placeholder': 'Details', 'class': 'form-control', 'rows': '5'})
	)
