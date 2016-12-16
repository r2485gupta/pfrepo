from django.shortcuts import render, render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, check_password
from django.contrib.auth.hashers import make_password
from django.conf import settings
from api.models import *
from api.forms import *
import os
import json
import pdfcrowd

def login_user(request):
	if request.method == 'POST' and 'loginForm' in request.POST:
		l_form = loginForm(request.POST)
		s_form = signupForm()
		if l_form.is_valid():
			email = l_form.cleaned_data['email']
			password = l_form.cleaned_data['password']

			try:
				user_obj = User.objects.get(email=email)
			except:
				user_is_valid = False
				status = {
					'error': True,
					'error_message': 'Invalid Username or Password!',
					'success': False,
					'success_message': '',
				}				
				variables = RequestContext(request, {
					'status': status,
					'loginForm': l_form,
					'signupForm':  s_form
				})
				return render_to_response('signup-page.html', variables)

			username = user_obj.username
			user = authenticate(username = username, password = password)

			if user == None:
				user_is_valid = False
				status = {
					'error': True,
					'error_message': 'Invalid Username or Password!',
					'success': False,
					'success_message': '',
				}
				variables = RequestContext(request, {
					'status': status,
					'loginForm': l_form,
					'signupForm': s_form
				})
				return render_to_response('signup-page.html', variables)
			else:
				user_is_valid = True
				login(request, user)
				return HttpResponseRedirect('/profile/' + username)
		else:
			user_is_valid = False
			status = {
				'error': True,
				'error_message': 'Invalid Username or Password!',
				'success': False,
				'success_message': '',
			}
			variables = RequestContext(request, {
				'status': status,
				'loginForm': l_form,
				'signupForm': s_form
			})
			return HttpResponseRedirect('/error/')
			return render_to_response('signup-page.html', variables)

	elif request.method == 'POST' and 'signupForm' in request.POST:
		l_form = loginForm()
		s_form = signupForm(request.POST)
		existing_user = True

		if s_form.is_valid():
			user_name = s_form.cleaned_data['user_name']
			email = s_form.cleaned_data['email']
			password = make_password(s_form.cleaned_data['password'])

			try:
				user_obj = User.objects.get(username=username, email=email)
			except:
				existing_user = False

			if(existing_user == True):
				status = {
					'error': True,
					'error_message': 'An Account with similar Mail ID already exists.',
					'success': False,
					'success_message': '',
				}
				variables = RequestContext(request, {
					'status': status,
					'loginForm': l_form,
					'signupForm': s_form
				})
				return render_to_response('signup-page.html', variables)
			else:
				new_User = User(
					username = user_name,
					email = email,			
					password = password
				)
				new_User.save()
				new_user = user_details(
					user_id = new_User 
				)
				new_user.save()
				return HttpResponseRedirect('/profile/' + user_name)
		else:
			user_is_valid = False
			status = {
				'error': True,
				'error_message': 'Invalid Username or Password!',
				'success': False,
				'success_message': '',
			}
			variables = RequestContext(request, {
				'status': status,
				'loginForm': l_form,
				'signupForm': s_form
			})
			return render_to_response('signup-page.html', variables)
	else:
		error = "ERROR"
		l_form = loginForm()
		s_form = signupForm()
		variables = RequestContext(request, {
			'loginForm': l_form,
			'signupForm': s_form,
			'error': 'error'
		})
		return render_to_response('signup-page.html', variables)

def profile(request, username):
	User_obj = User.objects.get(username = username)
	if request.method=='GET' and 'workForm' in request.GET:
		workForm = profile_workForm(request.GET)
		if workForm.is_valid():
			work_type = workForm.cleaned_data['work_type']
			if work_type == 'Internship':
				company_name = workForm.cleaned_data['internship_company_name']
				from_date = workForm.cleaned_data['internship_from_date']
				to_date = workForm.cleaned_data['internship_to_date']
				title = workForm.cleaned_data['internship_title']

				formatted_from_date = from_date[6:] +'-'+ from_date[0:2] +'-'+ from_date[3:5]
				formatted_to_date = to_date[6:] +'-'+ to_date[0:2] +'-'+ to_date[3:5]

				work_obj = work(
					user_id = User_obj,
					work_type = work_type,
					internship_company_name = company_name,
					internship_date_from = formatted_from_date,
					internship_date_to = formatted_to_date,
					internship_title = title,
				)
				work_obj.save()
				status = {
					'error': False,
					'error_message': '',
					'success': True,
					'success_message': 'Work details saved.',
				}
				workForm = profile_workForm()
				educationForm = profile_educationForm()
				certificationForm = profile_certificationForm()
				publicationForm = profile_publicationForm()
				extracurricularForm = profile_extracurricularForm()
				patentForm = profile_patentForm()
				achievementForm = profile_achievementForm()
				aboutForm = profile_aboutmeForm()
				educationaddForm = profile_education_add_editForm()
				workaddForm = profile_work_add_editForm()
				extracurricularaddForm = profile_extracurricular_add_editForm()
				certificationaddForm = profile_certification_add_editForm()
				achievementsaddForm = profile_achievements_add_editForm()
				publicationaddForm = profile_publications_add_editForm()
				patentaddForm = profile_patent_add_editForm()
				variables = RequestContext(request, {
					'workForm': workForm,
					'educationForm': educationForm,
					'certificationForm': certificationForm,
					'publicationForm': publicationForm,
					'extracurricularForm': extracurricularForm,
					'patentForm': patentForm,
					'achievementForm': achievementForm,
					'aboutForm': aboutForm,
					'educationaddForm': educationaddForm,
					'workaddForm': workaddForm,
					'extracurricularaddForm': extracurricularaddForm,
					'certificationaddForm': certificationaddForm,
					'achievementsaddForm': achievementsaddForm,
					'publicationaddForm': publicationaddForm,
					'patentaddForm': patentaddForm,
					'status': status
				})
				return render_to_response('profile-page.html', variables)

			elif work_type == 'Job':
				from_date = workForm.cleaned_data['job_from_date']
				to_date = workForm.cleaned_data['job_to_date']
				company_name = workForm.cleaned_data['job_company_name']
				designation = workForm.cleaned_data['job_designation']

				formatted_from_date = from_date[6:] +'-'+ from_date[0:2] +'-'+ from_date[3:5]
				formatted_to_date = to_date[6:] +'-'+ to_date[0:2] +'-'+ to_date[3:5]

				work_obj = work(
					user_id = User_obj,
					work_type = work_type,
					job_date_from = from_date,
					job_date_to = to_date,
					job_company_name = company_name,
					job_designation = designation
				)
				work_obj.save()
				status = {
					'error': False,
					'error_message': '',
					'success': True,
					'success_message': 'Work details saved.',
				}
				workForm = profile_workForm()
				educationForm = profile_educationForm()
				certificationForm = profile_certificationForm()
				publicationForm = profile_publicationForm()
				extracurricularForm = profile_extracurricularForm()
				patentForm = profile_patentForm()
				achievementForm = profile_achievementForm()
				aboutForm = profile_aboutmeForm()
				educationaddForm = profile_education_add_editForm()
				workaddForm = profile_work_add_editForm()
				extracurricularaddForm = profile_extracurricular_add_editForm()
				certificationaddForm = profile_certification_add_editForm()
				achievementsaddForm = profile_achievements_add_editForm()
				publicationaddForm = profile_publications_add_editForm()
				patentaddForm = profile_patent_add_editForm()
				variables = RequestContext(request, {
					'workForm': workForm,
					'educationForm': educationForm,
					'certificationForm': certificationForm,
					'publicationForm': publicationForm,
					'extracurricularForm': extracurricularForm,
					'patentForm': patentForm,
					'achievementForm': achievementForm,
					'aboutForm': aboutForm,
					'educationaddForm': educationaddForm,
					'workaddForm': workaddForm,
					'extracurricularaddForm': extracurricularaddForm,
					'certificationaddForm': certificationaddForm,
					'achievementsaddForm': achievementsaddForm,
					'publicationaddForm': publicationaddForm,
					'patentaddForm': patentaddForm,
					'status': status
				})
				return render_to_response('profile-page.html', variables)

			else:
				client = workForm.cleaned_data['freelancer_client']
				title = workForm.cleaned_data['freelancer_project_title']
				status = workForm.cleaned_data['freelancer_project_status']
				link = workForm.cleaned_data['freelancer_link']

				work_obj = work(
					user_id = User_obj,
					work_type = 'Freelancer',
					freelancer_client_name = client,
					freelancer_project_title = title,
					freelancer_status = status,
					freelancer_link = link
				)
				work_obj.save()
				status = {
					'error': False,
					'error_message': '',
					'success': True,
					'success_message': 'Work details saved.',
				}
				workForm = profile_workForm()
				educationForm = profile_educationForm()
				certificationForm = profile_certificationForm()
				publicationForm = profile_publicationForm()
				extracurricularForm = profile_extracurricularForm()
				patentForm = profile_patentForm()
				achievementForm = profile_achievementForm()
				aboutForm = profile_aboutmeForm()
				educationaddForm = profile_education_add_editForm()
				workaddForm = profile_work_add_editForm()
				extracurricularaddForm = profile_extracurricular_add_editForm()
				certificationaddForm = profile_certification_add_editForm()
				achievementsaddForm = profile_achievements_add_editForm()
				publicationaddForm = profile_publications_add_editForm()
				patentaddForm = profile_patent_add_editForm()
				variables = RequestContext(request, {
					'workForm': workForm,
					'educationForm': educationForm,
					'certificationForm': certificationForm,
					'publicationForm': publicationForm,
					'extracurricularForm': extracurricularForm,
					'patentForm': patentForm,
					'achievementForm': achievementForm,
					'aboutForm': aboutForm,
					'educationaddForm': educationaddForm,
					'workaddForm': workaddForm,
					'extracurricularaddForm': extracurricularaddForm,
					'certificationaddForm': certificationaddForm,
					'achievementsaddForm': achievementsaddForm,
					'publicationaddForm': publicationaddForm,
					'patentaddForm': patentaddForm,
					'status': status
				})
				return render_to_response('profile-page.html', variables)

	elif request.method=='GET' and 'educationForm' in request.GET:
		educationForm = profile_educationForm(request.GET)
		if educationForm.is_valid():
			year = educationForm.cleaned_data['year']
			education_type = educationForm.cleaned_data['education_type']
			institution = educationForm.cleaned_data['institution']
			aggregate = educationForm.cleaned_data['aggregate']
			what_did_you_do_there = educationForm.cleaned_data['what_did_you_do_there']
			# attached_file = request.FILES['attach_file']

			education_obj = education(
				user_id = User_obj,
				year = year,
				education_type = education_type,
				institution_name = institution,
				aggregate = aggregate,
				what_did_you_do_there = what_did_you_do_there
				# document = attached_file
			)
			education_obj.save()
			status = {
				'error': False,
				'error_message': '',
				'success': True,
				'success_message': 'Education details saved.',
			}
			workForm = profile_workForm()
			educationForm = profile_educationForm()
			certificationForm = profile_certificationForm()
			publicationForm = profile_publicationForm()
			extracurricularForm = profile_extracurricularForm()
			patentForm = profile_patentForm()
			achievementForm = profile_achievementForm()
			aboutForm = profile_aboutmeForm()
			educationaddForm = profile_education_add_editForm()
			workaddForm = profile_work_add_editForm()
			extracurricularaddForm = profile_extracurricular_add_editForm()
			certificationaddForm = profile_certification_add_editForm()
			achievementsaddForm = profile_achievements_add_editForm()
			publicationaddForm = profile_publications_add_editForm()
			patentaddForm = profile_patent_add_editForm()
			variables = RequestContext(request, {
				'workForm': workForm,
				'educationForm': educationForm,
				'certificationForm': certificationForm,
				'publicationForm': publicationForm,
				'extracurricularForm': extracurricularForm,
				'patentForm': patentForm,
				'achievementForm': achievementForm,
				'aboutForm': aboutForm,
				'educationaddForm': educationaddForm,
				'workaddForm': workaddForm,
				'extracurricularaddForm': extracurricularaddForm,
				'certificationaddForm': certificationaddForm,
				'achievementsaddForm': achievementsaddForm,
				'publicationaddForm': publicationaddForm,
				'patentaddForm': patentaddForm,
				'status': status
			})
			return render_to_response('profile-page.html', variables)
		# else:
		# 	return HttpResponseRedirect('/error')

	elif request.method=='GET' and 'certificationForm' in request.GET:
		certificationForm = profile_certificationForm(request.GET)
		if certificationForm.is_valid():
			year = certificationForm.cleaned_data['year']
			agency = certificationForm.cleaned_data['agency']
			mode = certificationForm.cleaned_data['mode']
			details = certificationForm.cleaned_data['details']
			# attached_file = request.FILES['attach_file']

			certification_obj = certification(
				user_id = User_obj,
				year = year,
				agency = agency,
				mode_of_certification = mode,
				details = details,
				# document = attached_file
			)
			certification_obj.save()
			status = {
				'error': False,
				'error_message': '',
				'success': True,
				'success_message': 'Certification details saved.',
			}
			workForm = profile_workForm()
			educationForm = profile_educationForm()
			certificationForm = profile_certificationForm()
			publicationForm = profile_publicationForm()
			extracurricularForm = profile_extracurricularForm()
			patentForm = profile_patentForm()
			achievementForm = profile_achievementForm()
			aboutForm = profile_aboutmeForm()
			educationaddForm = profile_education_add_editForm()
			workaddForm = profile_work_add_editForm()
			extracurricularaddForm = profile_extracurricular_add_editForm()
			certificationaddForm = profile_certification_add_editForm()
			achievementsaddForm = profile_achievements_add_editForm()
			publicationaddForm = profile_publications_add_editForm()
			patentaddForm = profile_patent_add_editForm()
			variables = RequestContext(request, {
				'workForm': workForm,
				'educationForm': educationForm,
				'certificationForm': certificationForm,
				'publicationForm': publicationForm,
				'extracurricularForm': extracurricularForm,
				'patentForm': patentForm,
				'achievementForm': achievementForm,
				'aboutForm': aboutForm,
				'educationaddForm': educationaddForm,
				'workaddForm': workaddForm,
				'extracurricularaddForm': extracurricularaddForm,
				'certificationaddForm': certificationaddForm,
				'achievementsaddForm': achievementsaddForm,
				'publicationaddForm': publicationaddForm,
				'patentaddForm': patentaddForm,
				'status': status
			})
			return render_to_response('profile-page.html', variables)

	elif request.method=='GET' and 'publicationForm' in request.GET:
		publicationForm = profile_publicationForm(request.GET)
		if publicationForm.is_valid():
			year = publicationForm.cleaned_data['year']
			mode = publicationForm.cleaned_data['mode']
			journal = publicationForm.cleaned_data['journal']
			details = publicationForm.cleaned_data['details']
			status = publicationForm.cleaned_data['status']
			link = publicationForm.cleaned_data['link']

			publication_obj = publication(
				user_id = User_obj,
				year = year,
				mode = mode,
				journal = journal,
				details = details,
				status = status,
				link = link
			)
			publication_obj.save()
			status = {
				'error': False,
				'error_message': '',
				'success': True,
				'success_message': 'Publication details saved.',
			}
			workForm = profile_workForm()
			educationForm = profile_educationForm()
			certificationForm = profile_certificationForm()
			publicationForm = profile_publicationForm()
			extracurricularForm = profile_extracurricularForm()
			patentForm = profile_patentForm()
			achievementForm = profile_achievementForm()
			aboutForm = profile_aboutmeForm()
			educationaddForm = profile_education_add_editForm()
			workaddForm = profile_work_add_editForm()
			extracurricularaddForm = profile_extracurricular_add_editForm()
			certificationaddForm = profile_certification_add_editForm()
			achievementsaddForm = profile_achievements_add_editForm()
			publicationaddForm = profile_publications_add_editForm()
			patentaddForm = profile_patent_add_editForm()
			variables = RequestContext(request, {
				'workForm': workForm,
				'educationForm': educationForm,
				'certificationForm': certificationForm,
				'publicationForm': publicationForm,
				'extracurricularForm': extracurricularForm,
				'patentForm': patentForm,
				'achievementForm': achievementForm,
				'aboutForm': aboutForm,
				'educationaddForm': educationaddForm,
				'workaddForm': workaddForm,
				'extracurricularaddForm': extracurricularaddForm,
				'certificationaddForm': certificationaddForm,
				'achievementsaddForm': achievementsaddForm,
				'publicationaddForm': publicationaddForm,
				'patentaddForm': patentaddForm,
				'status': status
			})
			return render_to_response('profile-page.html', variables)

	elif request.method=='GET' and 'extracurricularForm' in request.GET:
		extracurricularForm = profile_extracurricularForm(request.GET)
		if extracurricularForm.is_valid():
			year = extracurricularForm.cleaned_data['year']
			activity_type = extracurricularForm.cleaned_data['activity_type']
			title = extracurricularForm.cleaned_data['title']
			details = extracurricularForm.cleaned_data['details']
			organization = extracurricularForm.cleaned_data['organization']
			link = extracurricularForm.cleaned_data['link']

			extracurricular_obj = extracurricular_activities(
				user_id = User_obj,
				year = year,
				activity_type = activity_type,
				activity_details = details,
				title = title,
				organization = organization,
				link = link
			)
			extracurricular_obj.save()
			status = {
				'error': False,
				'error_message': '',
				'success': True,
				'success_message': 'Extracurricular details saved.',
			}
			workForm = profile_workForm()
			educationForm = profile_educationForm()
			certificationForm = profile_certificationForm()
			publicationForm = profile_publicationForm()
			extracurricularForm = profile_extracurricularForm()
			patentForm = profile_patentForm()
			achievementForm = profile_achievementForm()
			aboutForm = profile_aboutmeForm()
			educationaddForm = profile_education_add_editForm()
			workaddForm = profile_work_add_editForm()
			extracurricularaddForm = profile_extracurricular_add_editForm()
			certificationaddForm = profile_certification_add_editForm()
			achievementsaddForm = profile_achievements_add_editForm()
			publicationaddForm = profile_publications_add_editForm()
			patentaddForm = profile_patent_add_editForm()
			variables = RequestContext(request, {
				'workForm': workForm,
				'educationForm': educationForm,
				'certificationForm': certificationForm,
				'publicationForm': publicationForm,
				'extracurricularForm': extracurricularForm,
				'patentForm': patentForm,
				'achievementForm': achievementForm,
				'aboutForm': aboutForm,
				'educationaddForm': educationaddForm,
				'workaddForm': workaddForm,
				'extracurricularaddForm': extracurricularaddForm,
				'certificationaddForm': certificationaddForm,
				'achievementsaddForm': achievementsaddForm,
				'publicationaddForm': publicationaddForm,
				'patentaddForm': patentaddForm,
				'status': status
			})
			return render_to_response('profile-page.html', variables)

	elif request.method=='GET' and 'patentForm' in request.GET:
		patentForm = profile_patentForm(request.GET)
		if patentForm.is_valid():
			year = patentForm.cleaned_data['year']
			mode = patentForm.cleaned_data['mode']
			status = patentForm.cleaned_data['status']
			details = patentForm.cleaned_data['details']

			patent_obj = patent(
				user_id = User_obj,
				year = year,
				mode = mode,
				patent_details = details,
				patent_status = status
			)
			patent_obj.save()
			status = {
				'error': False,
				'error_message': '',
				'success': True,
				'success_message': 'Patent details saved.',
			}
			workForm = profile_workForm()
			educationForm = profile_educationForm()
			certificationForm = profile_certificationForm()
			publicationForm = profile_publicationForm()
			extracurricularForm = profile_extracurricularForm()
			patentForm = profile_patentForm()
			achievementForm = profile_achievementForm()
			aboutForm = profile_aboutmeForm()
			educationaddForm = profile_education_add_editForm()
			workaddForm = profile_work_add_editForm()
			extracurricularaddForm = profile_extracurricular_add_editForm()
			certificationaddForm = profile_certification_add_editForm()
			achievementsaddForm = profile_achievements_add_editForm()
			publicationaddForm = profile_publications_add_editForm()
			patentaddForm = profile_patent_add_editForm()
			variables = RequestContext(request, {
				'workForm': workForm,
				'educationForm': educationForm,
				'certificationForm': certificationForm,
				'publicationForm': publicationForm,
				'extracurricularForm': extracurricularForm,
				'patentForm': patentForm,
				'achievementForm': achievementForm,
				'aboutForm': aboutForm,
				'educationaddForm': educationaddForm,
				'workaddForm': workaddForm,
				'extracurricularaddForm': extracurricularaddForm,
				'certificationaddForm': certificationaddForm,
				'achievementsaddForm': achievementsaddForm,
				'publicationaddForm': publicationaddForm,
				'patentaddForm': patentaddForm,
				'status': status
			})
			return render_to_response('profile-page.html', variables)

	elif request.method=='GET' and 'achievementForm' in request.GET:
		achievementForm = profile_achievementForm(request.GET)
		if achievementForm.is_valid():
			year = achievementForm.cleaned_data['year']
			achievement_type = achievementForm.cleaned_data['achievement_type']
			title = achievementForm.cleaned_data['title']
			organization = achievementForm.cleaned_data['organization']
			details = achievementForm.cleaned_data['details']
			link = achievementForm.cleaned_data['link']
			# attached_file = request.FILES['attach_file']

			achievement_obj = achievements(
				user_id = User_obj,
				year = year,
				achievement_type = achievement_type,
				title = title,
				organization = organization,
				details = details,
				link = link,
				# document = attached_file
			)
			achievement_obj.save()
			status = {
				'error': False,
				'error_message': '',
				'success': True,
				'success_message': 'Achievement details saved.',
			}
			workForm = profile_workForm()
			educationForm = profile_educationForm()
			certificationForm = profile_certificationForm()
			publicationForm = profile_publicationForm()
			extracurricularForm = profile_extracurricularForm()
			patentForm = profile_patentForm()
			achievementForm = profile_achievementForm()
			aboutForm = profile_aboutmeForm()
			educationaddForm = profile_education_add_editForm()
			workaddForm = profile_work_add_editForm()
			extracurricularaddForm = profile_extracurricular_add_editForm()
			certificationaddForm = profile_certification_add_editForm()
			achievementsaddForm = profile_achievements_add_editForm()
			publicationaddForm = profile_publications_add_editForm()
			patentaddForm = profile_patent_add_editForm()
			variables = RequestContext(request, {
				'workForm': workForm,
				'educationForm': educationForm,
				'certificationForm': certificationForm,
				'publicationForm': publicationForm,
				'extracurricularForm': extracurricularForm,
				'patentForm': patentForm,
				'achievementForm': achievementForm,
				'aboutForm': aboutForm,
				'educationaddForm': educationaddForm,
				'workaddForm': workaddForm,
				'extracurricularaddForm': extracurricularaddForm,
				'certificationaddForm': certificationaddForm,
				'achievementsaddForm': achievementsaddForm,
				'publicationaddForm': publicationaddForm,
				'patentaddForm': patentaddForm,
				'status': status
			})
			return render_to_response('profile-page.html', variables)

	elif request.method=='GET' and 'workeditForm' in request.GET:
		workaddForm = profile_work_add_editForm(request.GET)
		if workaddForm.is_valid():
			work_type = workaddForm.cleaned_data['work_type']
			if work_type == 'Internship':
				row_id = workaddForm.cleaned_data['tuple_id']
				company_name = workaddForm.cleaned_data['internship_company_name']
				from_date = workaddForm.cleaned_data['internship_from_date']
				to_date = workaddForm.cleaned_data['internship_to_date']
				title = workaddForm.cleaned_data['internship_title']

				formatted_from_date = from_date[6:] +'-'+ from_date[0:2] +'-'+ from_date[3:5]
				formatted_to_date = to_date[6:] +'-'+ to_date[0:2] +'-'+ to_date[3:5]

				work_obj = work.objects.get(id = row_id)
				work_obj.internship_company_name = company_name
				work_obj.internship_from_date = formatted_from_date
				work_obj.internship_to_date = formatted_to_date
				work_obj.internship_title = title

				work_obj.save()
				
				status = {
					'error': False,
					'error_message': '',
					'success': True,
					'success_message': 'Work details saved.',
				}
				workForm = profile_workForm()
				educationForm = profile_educationForm()
				certificationForm = profile_certificationForm()
				publicationForm = profile_publicationForm()
				extracurricularForm = profile_extracurricularForm()
				patentForm = profile_patentForm()
				achievementForm = profile_achievementForm()
			
				t_educationData = education.objects.filter(user_id = User_obj)
				if len(t_educationData) == 0:
					t_educationData = 'unavailable'
				else:
					t_educationData = zip(t_educationData, range(len(t_educationData)))
				t_workData = work.objects.filter(user_id = User_obj)
				if len(t_workData) == 0:
					t_workData = 'unavailable'
				else:
					t_workData = zip(t_workData, range(len(t_workData)))
				t_certificationData = certification.objects.filter(user_id = User_obj)
				if len(t_certificationData) == 0:
					t_certificationData = 'unavailable'
				else:
					t_certificationData = zip(t_certificationData, range(len(t_certificationData)))
				t_extracurricularData = extracurricular_activities.objects.filter(user_id = User_obj)
				if len(t_extracurricularData) == 0:
					t_extracurricularData = 'unavailable'
				else:
					t_extracurricularData = zip(t_extracurricularData, range(len(t_extracurricularData)))
				t_achievementData = achievements.objects.filter(user_id = User_obj)
				if len(t_achievementData) == 0:
					t_achievementData = 'unavailable'
				else:
					t_achievementData = zip(t_achievementData, range(len(t_achievementData)))
				t_publicationData = publication.objects.filter(user_id = User_obj)
				if len(t_publicationData) == 0:
					t_publicationData = 'unavailable'
				else:
					t_publicationData = zip(t_publicationData, range(len(t_publicationData)))
				t_patentData = patent.objects.filter(user_id = User_obj)					
				if len(t_patentData) == 0:
					t_patentData = 'unavailable'
				else:
					t_patentData = zip(t_patentData, range(len(t_patentData)))
				
				# aboutForm population
				try:
					existing_about = user_details.objects.get(user_id = User_obj)
				except:
					existing_about = 'unavailable'
				if existing_about!='unavailable':
					aboutForm_existing = {
						'profession': existing_about.profession,
						'first_name': existing_about.first_name,
						'last_name': existing_about.last_name,
						'dob': existing_about.dob,
						'short_bio': existing_about.short_bio,
						'facebook_url': existing_about.facebook_url,
						'twitter_handle': existing_about.twitter_handle,
						'linkedin_url': existing_about.linkedin_url
					}
				else:
					aboutForm_existing = None
				aboutData_existing = aboutForm_existing
				aboutForm = profile_aboutmeForm(aboutForm_existing)

				#educationForm population and edit
				educationData = education.objects.filter(user_id = User_obj)
				if len(educationData) == 0:
					educationData = 'unavailable'
					educationInfoForm = None
				else:
					copy_educationData = educationData
					educationDataCounter = range(len(copy_educationData))
					educationData = zip(copy_educationData, educationDataCounter)
					educationEditForm = []
					for e in copy_educationData:
						e_dict = {
							'tuple_id': e.id,
							'year': e.year,
							'education_type': e.education_type,
							'institution': e.institution_name,
							'aggregate': e.aggregate,
							'what_did_you_do_there': e.what_did_you_do_there
						}
						el = profile_education_add_editForm(e_dict)
						educationEditForm.append(el)
					educationInfoForm = zip(educationEditForm, educationDataCounter)
				educationaddForm = profile_education_add_editForm()

				#workForm population and edit
				workData = work.objects.filter(user_id = User_obj)
				if len(workData) == 0:
					workData = 'unavailable'
					workInfoForm = None
				else:
					copy_workData = workData
					workDataCounter = range(len(copy_workData))
					workData = zip(copy_workData, workDataCounter)
					workEditForm = []
					for w in copy_workData:
						if w.work_type == 'Internship':
							w_dict = {
								'tuple_id': w.id,
								'work_type': w.work_type,
								'internship_company_name': w.internship_company_name,
								'internship_from_date': w.internship_date_from,
								'internship_to_date': w.internship_date_to,
								'internship_title': w.internship_title
							}
						elif w.work_type == 'Job':
							w_dict = {
								'tuple_id': w.id,
								'work_type': w.work_type,
								'job_company_name': w.job_company_name,
								'job_designation': w.job_designation,
								'job_from_date': w.job_date_from,
								'job_to_date': w.job_date_to
							}
						else:
							w_dict = {
								'tuple_id': w.id,
								'work_type': w.work_type,
								'freelancer_client': w.freelancer_client_name,
								'freelancer_project_title': w.freelancer_project_title,
								'freelancer_link': w.freelancer_link,
								'freelancer_project_status': w.freelancer_status,
								'freelancer_year': w.freelancer_year
							}
						wl = profile_work_add_editForm(w_dict)
						workEditForm.append(wl)
					workInfoForm = zip(workEditForm, workDataCounter)
				workaddForm = profile_work_add_editForm()

				#certificationForm populate and edit
				certificationData = certification.objects.filter(user_id = User_obj)
				if len(certificationData) == 0:
					certificationData = 'unavailable'
					certificationInfoForm = None
				else:
					copy_certificationData = certificationData
					certificationDataCounter = range(len(copy_certificationData))
					certificationData = zip(copy_certificationData, certificationDataCounter)
					certificationEditForm = []
					for c in copy_certificationData:
						c_dict = {
							'tuple_id': c.id,
							'year': c.year,
							'agency': c.agency,
							'mode': c.mode_of_certification,
							'details': c.details,					
						}		
						wl = profile_certification_add_editForm(c_dict)
						certificationEditForm.append(wl)
					certificationInfoForm = zip(certificationEditForm, certificationDataCounter)
				certificationaddForm = profile_certification_add_editForm()

				#extracurricularForm populate and edit
				exData = extracurricular_activities.objects.filter(user_id = User_obj)
				if len(exData) == 0:
					exData = 'unavailable'
					exInfoForm = None
				else:
					copy_exData = exData
					exDataCounter = range(len(copy_exData))
					exData = zip(copy_exData, exDataCounter)
					exEditForm = []
					for e in copy_exData:
						e_dict = {
							'tuple_id': e.id,
							'year': e.year,
							'activity_type': e.activity_type,
							'title': e.title,
							'details': e.activity_details,
							'organization': e.organization,
							'link': e.link					
						}			
						wl = profile_extracurricular_add_editForm(e_dict)
						exEditForm.append(wl)
					exInfoForm = zip(exEditForm, exDataCounter)
				extracurricularaddForm = profile_extracurricular_add_editForm()

				#achievementForm populate and edit
				achData = achievements.objects.filter(user_id = User_obj)
				if len(achData) == 0:
					achData = 'unavailable'
					achInfoForm = None
				else:
					copy_achData = achData
					achDataCounter = range(len(copy_achData))
					achData = zip(copy_achData, achDataCounter)
					achEditForm = []
					for a in copy_achData:
						a_dict = {
							'tuple_id': a.id,
							'year': a.year,
							'achievement_type': a.achievement_type,
							'title': a.title,
							'details': a.details,
							'organization': a.organization,
							'link': a.link					
						}			
						wl = profile_achievements_add_editForm(a_dict)
						achEditForm.append(wl)
					achInfoForm = zip(achEditForm, achDataCounter)
				achievementsaddForm = profile_achievements_add_editForm()

				#publicationForm populate and edit
				pubData = publication.objects.filter(user_id = User_obj)
				if len(pubData) == 0:
					pubData = 'unavailable'
					pubInfoForm = None
				else:
					copy_pubData = pubData
					pubDataCounter = range(len(copy_pubData))
					pubData = zip(copy_pubData, pubDataCounter)
					pubEditForm = []
					for p in copy_pubData:
						p_dict = {
							'tuple_id': p.id,
							'year': p.year,
							'mode': p.mode,
							'journal': p.journal,
							'status': p.status,				
							'details': p.details,					
							'link': p.link					
						}			
						wl = profile_publications_add_editForm(p_dict)
						pubEditForm.append(wl)
					pubInfoForm = zip(pubEditForm, pubDataCounter)
				publicationaddForm = profile_publications_add_editForm()

				#patentForm populate and edit
				patData = patent.objects.filter(user_id = User_obj)
				if len(patData) == 0:
					patData = 'unavailable'
					patInfoForm = None
				else:
					copy_patData = patData
					patDataCounter = range(len(copy_patData))
					patData = zip(copy_patData, patDataCounter)
					patEditForm = []
					for pa in copy_patData:
						pa_dict = {
							'tuple_id': pa.id,
							'year': pa.year,
							'mode': pa.mode,					
							'status': pa.patent_status,				
							'details': pa.patent_details
						}			
						wl = profile_patent_add_editForm(pa_dict)
						patEditForm.append(wl)
					patInfoForm = zip(patEditForm, patDataCounter)
				patentaddForm = profile_patent_add_editForm()

				#skillsForm populate and edit
				skillsData = skills.objects.filter(user_id = User_obj)
				if len(skillsData) == 0:
					skillsData = 'unavailable'
					skillsInfoForm = None
				else:
					counter = 1
					skill_name_text = ''
					for s in skillsData:
						if counter == 1:
							skill_name_text = s.skill_name
						else:
							skill_name_text = skill_name_text + ',' + s.skill_name
						counter = counter + 1

					s_dict = {
						'skill': skill_name_text
					}
					skillsInfoForm = profile_skills_add_editForm(s_dict)
				skillsaddForm = profile_skills_add_editForm()

				variables = RequestContext(request, {
					'workForm': workForm,
					'educationForm': educationForm,
					'certificationForm': certificationForm,
					'publicationForm': publicationForm,
					'extracurricularForm': extracurricularForm,
					'patentForm': patentForm,
					'achievementForm': achievementForm,
					'aboutForm': aboutForm,
					'educationaddForm': educationaddForm,
					'workaddForm': workaddForm,
					'extracurricularaddForm': extracurricularaddForm,
					'certificationaddForm': certificationaddForm,
					'achievementsaddForm': achievementsaddForm,
					'publicationaddForm': publicationaddForm,
					'patentaddForm': patentaddForm,
					'aboutData': aboutData_existing,
					'educationData': educationData,	
					'educationInfoForm': educationInfoForm,
					'workData': workData,
					'workInfoForm': workInfoForm,
					'certificationData': certificationData,
					'certificationInfoForm': certificationInfoForm,
					'exData': exData,
					'exInfoForm': exInfoForm,
					'achData': achData,
					'achInfoForm': achInfoForm,
					'pubData': pubData,
					'pubInfoForm': pubInfoForm,
					'patData': patData,
					'patInfoForm': patInfoForm,
					'skillsaddForm': skillsaddForm,
					'skillsData': skillsData,
					'skillsInfoForm': skillsInfoForm,
					't_educationData': t_educationData,
					't_workData': t_workData,
					't_certificationData': t_certificationData,
					't_extracurricularData': t_extracurricularData,
					't_achievementData': t_achievementData,
					't_publicationData': t_publicationData,
					't_patentData': t_patentData
				})
				return render_to_response('profile-page.html', variables)

			elif work_type == 'Job':
				row_id = workaddForm.cleaned_data['tuple_id']
				from_date = workaddForm.cleaned_data['job_from_date']
				to_date = workaddForm.cleaned_data['job_to_date']
				company_name = workaddForm.cleaned_data['job_company_name']
				designation = workaddForm.cleaned_data['job_designation']

				formatted_from_date = from_date[6:] +'-'+ from_date[0:2] +'-'+ from_date[3:5]
				formatted_to_date = to_date[6:] +'-'+ to_date[0:2] +'-'+ to_date[3:5]
		
				work_obj.job_date_from = formatted_from_date
				work_obj.job_date_to = formatted_to_date
				work_obj.job_company_name = company_name
				work_obj.job_designation = designation

				work_obj.save()
				status = {
					'error': False,
					'error_message': '',
					'success': True,
					'success_message': 'Work details saved.',
				}
				workForm = profile_workForm()
				educationForm = profile_educationForm()
				certificationForm = profile_certificationForm()
				publicationForm = profile_publicationForm()
				extracurricularForm = profile_extracurricularForm()
				patentForm = profile_patentForm()
				achievementForm = profile_achievementForm()
				t_educationData = education.objects.filter(user_id = User_obj)
				if len(t_educationData) == 0:
					t_educationData = 'unavailable'
				else:
					t_educationData = zip(t_educationData, range(len(t_educationData)))
				t_workData = work.objects.filter(user_id = User_obj)
				if len(t_workData) == 0:
					t_workData = 'unavailable'
				else:
					t_workData = zip(t_workData, range(len(t_workData)))
				t_certificationData = certification.objects.filter(user_id = User_obj)
				if len(t_certificationData) == 0:
					t_certificationData = 'unavailable'
				else:
					t_certificationData = zip(t_certificationData, range(len(t_certificationData)))
				t_extracurricularData = extracurricular_activities.objects.filter(user_id = User_obj)
				if len(t_extracurricularData) == 0:
					t_extracurricularData = 'unavailable'
				else:
					t_extracurricularData = zip(t_extracurricularData, range(len(t_extracurricularData)))
				t_achievementData = achievements.objects.filter(user_id = User_obj)
				if len(t_achievementData) == 0:
					t_achievementData = 'unavailable'
				else:
					t_achievementData = zip(t_achievementData, range(len(t_achievementData)))
				t_publicationData = publication.objects.filter(user_id = User_obj)
				if len(t_publicationData) == 0:
					t_publicationData = 'unavailable'
				else:
					t_publicationData = zip(t_publicationData, range(len(t_publicationData)))
				t_patentData = patent.objects.filter(user_id = User_obj)					
				if len(t_patentData) == 0:
					t_patentData = 'unavailable'
				else:
					t_patentData = zip(t_patentData, range(len(t_patentData)))

				
				# aboutForm population
				try:
					existing_about = user_details.objects.get(user_id = User_obj)
				except:
					existing_about = 'unavailable'
				if existing_about!='unavailable':
					aboutForm_existing = {
						'profession': existing_about.profession,
						'first_name': existing_about.first_name,
						'last_name': existing_about.last_name,
						'dob': existing_about.dob,
						'short_bio': existing_about.short_bio,
						'facebook_url': existing_about.facebook_url,
						'twitter_handle': existing_about.twitter_handle,
						'linkedin_url': existing_about.linkedin_url
					}
				else:
					aboutForm_existing = None
				aboutData_existing = aboutForm_existing
				aboutForm = profile_aboutmeForm(aboutForm_existing)

				#educationForm population and edit
				educationData = education.objects.filter(user_id = User_obj)
				if len(educationData) == 0:
					educationData = 'unavailable'
					educationInfoForm = None
				else:
					copy_educationData = educationData
					educationDataCounter = range(len(copy_educationData))
					educationData = zip(copy_educationData, educationDataCounter)
					educationEditForm = []
					for e in copy_educationData:
						e_dict = {
							'tuple_id': e.id,
							'year': e.year,
							'education_type': e.education_type,
							'institution': e.institution_name,
							'aggregate': e.aggregate,
							'what_did_you_do_there': e.what_did_you_do_there
						}
						el = profile_education_add_editForm(e_dict)
						educationEditForm.append(el)
					educationInfoForm = zip(educationEditForm, educationDataCounter)
				educationaddForm = profile_education_add_editForm()

				#workForm population and edit
				workData = work.objects.filter(user_id = User_obj)
				if len(workData) == 0:
					workData = 'unavailable'
					workInfoForm = None
				else:
					copy_workData = workData
					workDataCounter = range(len(copy_workData))
					workData = zip(copy_workData, workDataCounter)
					workEditForm = []
					for w in copy_workData:
						if w.work_type == 'Internship':
							w_dict = {
								'tuple_id': w.id,
								'work_type': w.work_type,
								'internship_company_name': w.internship_company_name,
								'internship_from_date': w.internship_date_from,
								'internship_to_date': w.internship_date_to,
								'internship_title': w.internship_title
							}
						elif w.work_type == 'Job':
							w_dict = {
								'tuple_id': w.id,
								'work_type': w.work_type,
								'job_company_name': w.job_company_name,
								'job_designation': w.job_designation,
								'job_from_date': w.job_date_from,
								'job_to_date': w.job_date_to
							}
						else:
							w_dict = {
								'tuple_id': w.id,
								'work_type': w.work_type,
								'freelancer_client': w.freelancer_client_name,
								'freelancer_project_title': w.freelancer_project_title,
								'freelancer_link': w.freelancer_link,
								'freelancer_project_status': w.freelancer_status,
								'freelancer_year': w.freelancer_year
							}
						wl = profile_work_add_editForm(w_dict)
						workEditForm.append(wl)
					workInfoForm = zip(workEditForm, workDataCounter)
				workaddForm = profile_work_add_editForm()

				#certificationForm populate and edit
				certificationData = certification.objects.filter(user_id = User_obj)
				if len(certificationData) == 0:
					certificationData = 'unavailable'
					certificationInfoForm = None
				else:
					copy_certificationData = certificationData
					certificationDataCounter = range(len(copy_certificationData))
					certificationData = zip(copy_certificationData, certificationDataCounter)
					certificationEditForm = []
					for c in copy_certificationData:
						c_dict = {
							'tuple_id': c.id,
							'year': c.year,
							'agency': c.agency,
							'mode': c.mode_of_certification,
							'details': c.details,					
						}		
						wl = profile_certification_add_editForm(c_dict)
						certificationEditForm.append(wl)
					certificationInfoForm = zip(certificationEditForm, certificationDataCounter)
				certificationaddForm = profile_certification_add_editForm()

				#extracurricularForm populate and edit
				exData = extracurricular_activities.objects.filter(user_id = User_obj)
				if len(exData) == 0:
					exData = 'unavailable'
					exInfoForm = None
				else:
					copy_exData = exData
					exDataCounter = range(len(copy_exData))
					exData = zip(copy_exData, exDataCounter)
					exEditForm = []
					for e in copy_exData:
						e_dict = {
							'tuple_id': e.id,
							'year': e.year,
							'activity_type': e.activity_type,
							'title': e.title,
							'details': e.activity_details,
							'organization': e.organization,
							'link': e.link					
						}			
						wl = profile_extracurricular_add_editForm(e_dict)
						exEditForm.append(wl)
					exInfoForm = zip(exEditForm, exDataCounter)
				extracurricularaddForm = profile_extracurricular_add_editForm()

				#achievementForm populate and edit
				achData = achievements.objects.filter(user_id = User_obj)
				if len(achData) == 0:
					achData = 'unavailable'
					achInfoForm = None
				else:
					copy_achData = achData
					achDataCounter = range(len(copy_achData))
					achData = zip(copy_achData, achDataCounter)
					achEditForm = []
					for a in copy_achData:
						a_dict = {
							'tuple_id': a.id,
							'year': a.year,
							'achievement_type': a.achievement_type,
							'title': a.title,
							'details': a.details,
							'organization': a.organization,
							'link': a.link					
						}			
						wl = profile_achievements_add_editForm(a_dict)
						achEditForm.append(wl)
					achInfoForm = zip(achEditForm, achDataCounter)
				achievementsaddForm = profile_achievements_add_editForm()

				#publicationForm populate and edit
				pubData = publication.objects.filter(user_id = User_obj)
				if len(pubData) == 0:
					pubData = 'unavailable'
					pubInfoForm = None
				else:
					copy_pubData = pubData
					pubDataCounter = range(len(copy_pubData))
					pubData = zip(copy_pubData, pubDataCounter)
					pubEditForm = []
					for p in copy_pubData:
						p_dict = {
							'tuple_id': p.id,
							'year': p.year,
							'mode': p.mode,
							'journal': p.journal,
							'status': p.status,				
							'details': p.details,					
							'link': p.link					
						}			
						wl = profile_publications_add_editForm(p_dict)
						pubEditForm.append(wl)
					pubInfoForm = zip(pubEditForm, pubDataCounter)
				publicationaddForm = profile_publications_add_editForm()

				#patentForm populate and edit
				patData = patent.objects.filter(user_id = User_obj)
				if len(patData) == 0:
					patData = 'unavailable'
					patInfoForm = None
				else:
					copy_patData = patData
					patDataCounter = range(len(copy_patData))
					patData = zip(copy_patData, patDataCounter)
					patEditForm = []
					for pa in copy_patData:
						pa_dict = {
							'tuple_id': pa.id,
							'year': pa.year,
							'mode': pa.mode,					
							'status': pa.patent_status,				
							'details': pa.patent_details
						}			
						wl = profile_patent_add_editForm(pa_dict)
						patEditForm.append(wl)
					patInfoForm = zip(patEditForm, patDataCounter)
				patentaddForm = profile_patent_add_editForm()

				skillsData = skills.objects.filter(user_id = User_obj)
				if len(skillsData) == 0:
					skillsData = 'unavailable'
					skillsInfoForm = None
				else:
					counter = 1
					skill_name_text = ''
					for s in skillsData:
						if counter == 1:
							skill_name_text = s.skill_name
						else:
							skill_name_text = skill_name_text + ',' + s.skill_name
						counter = counter + 1

					s_dict = {
						'skill': skill_name_text
					}
					skillsInfoForm = profile_skills_add_editForm(s_dict)
				skillsaddForm = profile_skills_add_editForm()

				variables = RequestContext(request, {
					'workForm': workForm,
					'educationForm': educationForm,
					'certificationForm': certificationForm,
					'publicationForm': publicationForm,
					'extracurricularForm': extracurricularForm,
					'patentForm': patentForm,
					'achievementForm': achievementForm,
					'aboutForm': aboutForm,
					'educationaddForm': educationaddForm,
					'workaddForm': workaddForm,
					'extracurricularaddForm': extracurricularaddForm,
					'certificationaddForm': certificationaddForm,
					'achievementsaddForm': achievementsaddForm,
					'publicationaddForm': publicationaddForm,
					'patentaddForm': patentaddForm,
					'aboutData': aboutData_existing,
					'educationData': educationData,	
					'educationInfoForm': educationInfoForm,
					'workData': workData,
					'workInfoForm': workInfoForm,
					'certificationData': certificationData,
					'certificationInfoForm': certificationInfoForm,
					'exData': exData,
					'exInfoForm': exInfoForm,
					'achData': achData,
					'achInfoForm': achInfoForm,
					'pubData': pubData,
					'pubInfoForm': pubInfoForm,
					'patData': patData,
					'patInfoForm': patInfoForm,
					'skillsaddForm': skillsaddForm,
					'skillsData': skillsData,
					'skillsInfoForm': skillsInfoForm,
					't_educationData': t_educationData,
					't_workData': t_workData,
					't_certificationData': t_certificationData,
					't_extracurricularData': t_extracurricularData,
					't_achievementData': t_achievementData,
					't_publicationData': t_publicationData,
					't_patentData': t_patentData
				})
				return render_to_response('profile-page.html', variables)

			else:
				row_id = workaddForm.cleaned_data['tuple_id']
				client = workaddForm.cleaned_data['freelancer_client']
				title = workaddForm.cleaned_data['freelancer_project_title']
				status = workaddForm.cleaned_data['freelancer_project_status']
				link = workaddForm.cleaned_data['freelancer_link']

				work_obj.freelancer_client_name = client
				work_obj.freelancer_project_title = title
				work_obj.freelancer_status = status
				work_obj.freelancer_link = link

				work_obj.save()
				status = {
					'error': False,
					'error_message': '',
					'success': True,
					'success_message': 'Work details saved.',
				}
				workForm = profile_workForm()
				educationForm = profile_educationForm()
				certificationForm = profile_certificationForm()
				publicationForm = profile_publicationForm()
				extracurricularForm = profile_extracurricularForm()
				patentForm = profile_patentForm()
				achievementForm = profile_achievementForm()
				t_educationData = education.objects.filter(user_id = User_obj)
				if len(t_educationData) == 0:
					t_educationData = 'unavailable'
				else:
					t_educationData = zip(t_educationData, range(len(t_educationData)))
				t_workData = work.objects.filter(user_id = User_obj)
				if len(t_workData) == 0:
					t_workData = 'unavailable'
				else:
					t_workData = zip(t_workData, range(len(t_workData)))
				t_certificationData = certification.objects.filter(user_id = User_obj)
				if len(t_certificationData) == 0:
					t_certificationData = 'unavailable'
				else:
					t_certificationData = zip(t_certificationData, range(len(t_certificationData)))
				t_extracurricularData = extracurricular_activities.objects.filter(user_id = User_obj)
				if len(t_extracurricularData) == 0:
					t_extracurricularData = 'unavailable'
				else:
					t_extracurricularData = zip(t_extracurricularData, range(len(t_extracurricularData)))
				t_achievementData = achievements.objects.filter(user_id = User_obj)
				if len(t_achievementData) == 0:
					t_achievementData = 'unavailable'
				else:
					t_achievementData = zip(t_achievementData, range(len(t_achievementData)))
				t_publicationData = publication.objects.filter(user_id = User_obj)
				if len(t_publicationData) == 0:
					t_publicationData = 'unavailable'
				else:
					t_publicationData = zip(t_publicationData, range(len(t_publicationData)))
				t_patentData = patent.objects.filter(user_id = User_obj)					
				if len(t_patentData) == 0:
					t_patentData = 'unavailable'
				else:
					t_patentData = zip(t_patentData, range(len(t_patentData)))


				
				# aboutForm population
				try:
					existing_about = user_details.objects.get(user_id = User_obj)
				except:
					existing_about = 'unavailable'
				if existing_about!='unavailable':
					aboutForm_existing = {
						'profession': existing_about.profession,
						'first_name': existing_about.first_name,
						'last_name': existing_about.last_name,
						'dob': existing_about.dob,
						'short_bio': existing_about.short_bio,
						'facebook_url': existing_about.facebook_url,
						'twitter_handle': existing_about.twitter_handle,
						'linkedin_url': existing_about.linkedin_url
					}
				else:
					aboutForm_existing = None
				aboutData_existing = aboutForm_existing
				aboutForm = profile_aboutmeForm(aboutForm_existing)

				#educationForm population and edit
				educationData = education.objects.filter(user_id = User_obj)
				if len(educationData) == 0:
					educationData = 'unavailable'
					educationInfoForm = None
				else:
					copy_educationData = educationData
					educationDataCounter = range(len(copy_educationData))
					educationData = zip(copy_educationData, educationDataCounter)
					educationEditForm = []
					for e in copy_educationData:
						e_dict = {
							'tuple_id': e.id,
							'year': e.year,
							'education_type': e.education_type,
							'institution': e.institution_name,
							'aggregate': e.aggregate,
							'what_did_you_do_there': e.what_did_you_do_there
						}
						el = profile_education_add_editForm(e_dict)
						educationEditForm.append(el)
					educationInfoForm = zip(educationEditForm, educationDataCounter)
				educationaddForm = profile_education_add_editForm()

				#workForm population and edit
				workData = work.objects.filter(user_id = User_obj)
				if len(workData) == 0:
					workData = 'unavailable'
					workInfoForm = None
				else:
					copy_workData = workData
					workDataCounter = range(len(copy_workData))
					workData = zip(copy_workData, workDataCounter)
					workEditForm = []
					for w in copy_workData:
						if w.work_type == 'Internship':
							w_dict = {
								'tuple_id': w.id,
								'work_type': w.work_type,
								'internship_company_name': w.internship_company_name,
								'internship_from_date': w.internship_date_from,
								'internship_to_date': w.internship_date_to,
								'internship_title': w.internship_title
							}
						elif w.work_type == 'Job':
							w_dict = {
								'tuple_id': w.id,
								'work_type': w.work_type,
								'job_company_name': w.job_company_name,
								'job_designation': w.job_designation,
								'job_from_date': w.job_date_from,
								'job_to_date': w.job_date_to
							}
						else:
							w_dict = {
								'tuple_id': w.id,
								'work_type': w.work_type,
								'freelancer_client': w.freelancer_client_name,
								'freelancer_project_title': w.freelancer_project_title,
								'freelancer_link': w.freelancer_link,
								'freelancer_project_status': w.freelancer_status,
								'freelancer_year': w.freelancer_year
							}
						wl = profile_work_add_editForm(w_dict)
						workEditForm.append(wl)
					workInfoForm = zip(workEditForm, workDataCounter)
				workaddForm = profile_work_add_editForm()

				#certificationForm populate and edit
				certificationData = certification.objects.filter(user_id = User_obj)
				if len(certificationData) == 0:
					certificationData = 'unavailable'
					certificationInfoForm = None
				else:
					copy_certificationData = certificationData
					certificationDataCounter = range(len(copy_certificationData))
					certificationData = zip(copy_certificationData, certificationDataCounter)
					certificationEditForm = []
					for c in copy_certificationData:
						c_dict = {
							'tuple_id': c.id,
							'year': c.year,
							'agency': c.agency,
							'mode': c.mode_of_certification,
							'details': c.details,					
						}		
						wl = profile_certification_add_editForm(c_dict)
						certificationEditForm.append(wl)
					certificationInfoForm = zip(certificationEditForm, certificationDataCounter)
				certificationaddForm = profile_certification_add_editForm()

				#extracurricularForm populate and edit
				exData = extracurricular_activities.objects.filter(user_id = User_obj)
				if len(exData) == 0:
					exData = 'unavailable'
					exInfoForm = None
				else:
					copy_exData = exData
					exDataCounter = range(len(copy_exData))
					exData = zip(copy_exData, exDataCounter)
					exEditForm = []
					for e in copy_exData:
						e_dict = {
							'tuple_id': e.id,
							'year': e.year,
							'activity_type': e.activity_type,
							'title': e.title,
							'details': e.activity_details,
							'organization': e.organization,
							'link': e.link					
						}			
						wl = profile_extracurricular_add_editForm(e_dict)
						exEditForm.append(wl)
					exInfoForm = zip(exEditForm, exDataCounter)
				extracurricularaddForm = profile_extracurricular_add_editForm()

				#achievementForm populate and edit
				achData = achievements.objects.filter(user_id = User_obj)
				if len(achData) == 0:
					achData = 'unavailable'
					achInfoForm = None
				else:
					copy_achData = achData
					achDataCounter = range(len(copy_achData))
					achData = zip(copy_achData, achDataCounter)
					achEditForm = []
					for a in copy_achData:
						a_dict = {
							'tuple_id': a.id,
							'year': a.year,
							'achievement_type': a.achievement_type,
							'title': a.title,
							'details': a.details,
							'organization': a.organization,
							'link': a.link					
						}			
						wl = profile_achievements_add_editForm(a_dict)
						achEditForm.append(wl)
					achInfoForm = zip(achEditForm, achDataCounter)
				achievementsaddForm = profile_achievements_add_editForm()

				#publicationForm populate and edit
				pubData = publication.objects.filter(user_id = User_obj)
				if len(pubData) == 0:
					pubData = 'unavailable'
					pubInfoForm = None
				else:
					copy_pubData = pubData
					pubDataCounter = range(len(copy_pubData))
					pubData = zip(copy_pubData, pubDataCounter)
					pubEditForm = []
					for p in copy_pubData:
						p_dict = {
							'tuple_id': p.id,
							'year': p.year,
							'mode': p.mode,
							'journal': p.journal,
							'status': p.status,				
							'details': p.details,					
							'link': p.link					
						}			
						wl = profile_publications_add_editForm(p_dict)
						pubEditForm.append(wl)
					pubInfoForm = zip(pubEditForm, pubDataCounter)
				publicationaddForm = profile_publications_add_editForm()

				#patentForm populate and edit
				patData = patent.objects.filter(user_id = User_obj)
				if len(patData) == 0:
					patData = 'unavailable'
					patInfoForm = None
				else:
					copy_patData = patData
					patDataCounter = range(len(copy_patData))
					patData = zip(copy_patData, patDataCounter)
					patEditForm = []
					for pa in copy_patData:
						pa_dict = {
							'tuple_id': pa.id,
							'year': pa.year,
							'mode': pa.mode,					
							'status': pa.patent_status,				
							'details': pa.patent_details
						}			
						wl = profile_patent_add_editForm(pa_dict)
						patEditForm.append(wl)
					patInfoForm = zip(patEditForm, patDataCounter)
				patentaddForm = profile_patent_add_editForm()

				skillsData = skills.objects.filter(user_id = User_obj)
				if len(skillsData) == 0:
					skillsData = 'unavailable'
					skillsInfoForm = None
				else:
					counter = 1
					skill_name_text = ''
					for s in skillsData:
						if counter == 1:
							skill_name_text = s.skill_name
						else:
							skill_name_text = skill_name_text + ',' + s.skill_name
						counter = counter + 1

					s_dict = {
						'skill': skill_name_text
					}
					skillsInfoForm = profile_skills_add_editForm(s_dict)
				skillsaddForm = profile_skills_add_editForm()

				variables = RequestContext(request, {
					'workForm': workForm,
					'educationForm': educationForm,
					'certificationForm': certificationForm,
					'publicationForm': publicationForm,
					'extracurricularForm': extracurricularForm,
					'patentForm': patentForm,
					'achievementForm': achievementForm,
					'aboutForm': aboutForm,
					'educationaddForm': educationaddForm,
					'workaddForm': workaddForm,
					'extracurricularaddForm': extracurricularaddForm,
					'certificationaddForm': certificationaddForm,
					'achievementsaddForm': achievementsaddForm,
					'publicationaddForm': publicationaddForm,
					'patentaddForm': patentaddForm,
					'aboutData': aboutData_existing,
					'educationData': educationData,	
					'educationInfoForm': educationInfoForm,
					'workData': workData,
					'workInfoForm': workInfoForm,
					'certificationData': certificationData,
					'certificationInfoForm': certificationInfoForm,
					'exData': exData,
					'exInfoForm': exInfoForm,
					'achData': achData,
					'achInfoForm': achInfoForm,
					'pubData': pubData,
					'pubInfoForm': pubInfoForm,
					'patData': patData,
					'patInfoForm': patInfoForm,
					'skillsaddForm': skillsaddForm,
					'skillsData': skillsData,
					'skillsInfoForm': skillsInfoForm,
					't_educationData': t_educationData,
					't_workData': t_workData,
					't_certificationData': t_certificationData,
					't_extracurricularData': t_extracurricularData,
					't_achievementData': t_achievementData,
					't_publicationData': t_publicationData,
					't_patentData': t_patentData
				})
				return render_to_response('profile-page.html', variables)

	elif request.method=='GET' and 'workdeleteForm' in request.GET:
		workaddForm = profile_work_add_editForm(request.GET)
		if workaddForm.is_valid():
			work_type = workaddForm.cleaned_data['work_type']
			if work_type == 'Internship':
				row_id = workaddForm.cleaned_data['tuple_id']
				# company_name = workaddForm.cleaned_data['internship_company_name']
				# from_date = workaddForm.cleaned_data['internship_from_date']
				# to_date = workaddForm.cleaned_data['internship_to_date']
				# title = workaddForm.cleaned_data['internship_title']

				# formatted_from_date = from_date[6:] +'-'+ from_date[0:2] +'-'+ from_date[3:5]
				# formatted_to_date = to_date[6:] +'-'+ to_date[0:2] +'-'+ to_date[3:5]

				work_obj = work.objects.get(id = row_id)				

				work_obj.delete()
				
				status = {
					'error': False,
					'error_message': '',
					'success': True,
					'success_message': 'Work details deleted.',
				}
				workForm = profile_workForm()
				educationForm = profile_educationForm()
				certificationForm = profile_certificationForm()
				publicationForm = profile_publicationForm()
				extracurricularForm = profile_extracurricularForm()
				patentForm = profile_patentForm()
				achievementForm = profile_achievementForm()

				t_educationData = education.objects.filter(user_id = User_obj)
				if len(t_educationData) == 0:
					t_educationData = 'unavailable'
				else:
					t_educationData = zip(t_educationData, range(len(t_educationData)))
				t_workData = work.objects.filter(user_id = User_obj)
				if len(t_workData) == 0:
					t_workData = 'unavailable'
				else:
					t_workData = zip(t_workData, range(len(t_workData)))
				t_certificationData = certification.objects.filter(user_id = User_obj)
				if len(t_certificationData) == 0:
					t_certificationData = 'unavailable'
				else:
					t_certificationData = zip(t_certificationData, range(len(t_certificationData)))
				t_extracurricularData = extracurricular_activities.objects.filter(user_id = User_obj)
				if len(t_extracurricularData) == 0:
					t_extracurricularData = 'unavailable'
				else:
					t_extracurricularData = zip(t_extracurricularData, range(len(t_extracurricularData)))
				t_achievementData = achievements.objects.filter(user_id = User_obj)
				if len(t_achievementData) == 0:
					t_achievementData = 'unavailable'
				else:
					t_achievementData = zip(t_achievementData, range(len(t_achievementData)))
				t_publicationData = publication.objects.filter(user_id = User_obj)
				if len(t_publicationData) == 0:
					t_publicationData = 'unavailable'
				else:
					t_publicationData = zip(t_publicationData, range(len(t_publicationData)))
				t_patentData = patent.objects.filter(user_id = User_obj)					
				if len(t_patentData) == 0:
					t_patentData = 'unavailable'
				else:
					t_patentData = zip(t_patentData, range(len(t_patentData)))


				
				# aboutForm population
				try:
					existing_about = user_details.objects.get(user_id = User_obj)
				except:
					existing_about = 'unavailable'
				if existing_about!='unavailable':
					aboutForm_existing = {
						'profession': existing_about.profession,
						'first_name': existing_about.first_name,
						'last_name': existing_about.last_name,
						'dob': existing_about.dob,
						'short_bio': existing_about.short_bio,
						'facebook_url': existing_about.facebook_url,
						'twitter_handle': existing_about.twitter_handle,
						'linkedin_url': existing_about.linkedin_url
					}
				else:
					aboutForm_existing = None
				aboutData_existing = aboutForm_existing
				aboutForm = profile_aboutmeForm(aboutForm_existing)

				#educationForm population and edit
				educationData = education.objects.filter(user_id = User_obj)
				if len(educationData) == 0:
					educationData = 'unavailable'
					educationInfoForm = None
				else:
					copy_educationData = educationData
					educationDataCounter = range(len(copy_educationData))
					educationData = zip(copy_educationData, educationDataCounter)
					educationEditForm = []
					for e in copy_educationData:
						e_dict = {
							'tuple_id': e.id,
							'year': e.year,
							'education_type': e.education_type,
							'institution': e.institution_name,
							'aggregate': e.aggregate,
							'what_did_you_do_there': e.what_did_you_do_there
						}
						el = profile_education_add_editForm(e_dict)
						educationEditForm.append(el)
					educationInfoForm = zip(educationEditForm, educationDataCounter)
				educationaddForm = profile_education_add_editForm()

				#workForm population and edit
				workData = work.objects.filter(user_id = User_obj)
				if len(workData) == 0:
					workData = 'unavailable'
					workInfoForm = None
				else:
					copy_workData = workData
					workDataCounter = range(len(copy_workData))
					workData = zip(copy_workData, workDataCounter)
					workEditForm = []
					for w in copy_workData:
						if w.work_type == 'Internship':
							w_dict = {
								'tuple_id': w.id,
								'work_type': w.work_type,
								'internship_company_name': w.internship_company_name,
								'internship_from_date': w.internship_date_from,
								'internship_to_date': w.internship_date_to,
								'internship_title': w.internship_title
							}
						elif w.work_type == 'Job':
							w_dict = {
								'tuple_id': w.id,
								'work_type': w.work_type,
								'job_company_name': w.job_company_name,
								'job_designation': w.job_designation,
								'job_from_date': w.job_date_from,
								'job_to_date': w.job_date_to
							}
						else:
							w_dict = {
								'tuple_id': w.id,
								'work_type': w.work_type,
								'freelancer_client': w.freelancer_client_name,
								'freelancer_project_title': w.freelancer_project_title,
								'freelancer_link': w.freelancer_link,
								'freelancer_project_status': w.freelancer_status,
								'freelancer_year': w.freelancer_year
							}
						wl = profile_work_add_editForm(w_dict)
						workEditForm.append(wl)
					workInfoForm = zip(workEditForm, workDataCounter)
				workaddForm = profile_work_add_editForm()

				#certificationForm populate and edit
				certificationData = certification.objects.filter(user_id = User_obj)
				if len(certificationData) == 0:
					certificationData = 'unavailable'
					certificationInfoForm = None
				else:
					copy_certificationData = certificationData
					certificationDataCounter = range(len(copy_certificationData))
					certificationData = zip(copy_certificationData, certificationDataCounter)
					certificationEditForm = []
					for c in copy_certificationData:
						c_dict = {
							'tuple_id': c.id,
							'year': c.year,
							'agency': c.agency,
							'mode': c.mode_of_certification,
							'details': c.details,					
						}		
						wl = profile_certification_add_editForm(c_dict)
						certificationEditForm.append(wl)
					certificationInfoForm = zip(certificationEditForm, certificationDataCounter)
				certificationaddForm = profile_certification_add_editForm()

				#extracurricularForm populate and edit
				exData = extracurricular_activities.objects.filter(user_id = User_obj)
				if len(exData) == 0:
					exData = 'unavailable'
					exInfoForm = None
				else:
					copy_exData = exData
					exDataCounter = range(len(copy_exData))
					exData = zip(copy_exData, exDataCounter)
					exEditForm = []
					for e in copy_exData:
						e_dict = {
							'tuple_id': e.id,
							'year': e.year,
							'activity_type': e.activity_type,
							'title': e.title,
							'details': e.activity_details,
							'organization': e.organization,
							'link': e.link					
						}			
						wl = profile_extracurricular_add_editForm(e_dict)
						exEditForm.append(wl)
					exInfoForm = zip(exEditForm, exDataCounter)
				extracurricularaddForm = profile_extracurricular_add_editForm()

				#achievementForm populate and edit
				achData = achievements.objects.filter(user_id = User_obj)
				if len(achData) == 0:
					achData = 'unavailable'
					achInfoForm = None
				else:
					copy_achData = achData
					achDataCounter = range(len(copy_achData))
					achData = zip(copy_achData, achDataCounter)
					achEditForm = []
					for a in copy_achData:
						a_dict = {
							'tuple_id': a.id,
							'year': a.year,
							'achievement_type': a.achievement_type,
							'title': a.title,
							'details': a.details,
							'organization': a.organization,
							'link': a.link					
						}			
						wl = profile_achievements_add_editForm(a_dict)
						achEditForm.append(wl)
					achInfoForm = zip(achEditForm, achDataCounter)
				achievementsaddForm = profile_achievements_add_editForm()

				#publicationForm populate and edit
				pubData = publication.objects.filter(user_id = User_obj)
				if len(pubData) == 0:
					pubData = 'unavailable'
					pubInfoForm = None
				else:
					copy_pubData = pubData
					pubDataCounter = range(len(copy_pubData))
					pubData = zip(copy_pubData, pubDataCounter)
					pubEditForm = []
					for p in copy_pubData:
						p_dict = {
							'tuple_id': p.id,
							'year': p.year,
							'mode': p.mode,
							'journal': p.journal,
							'status': p.status,				
							'details': p.details,					
							'link': p.link					
						}			
						wl = profile_publications_add_editForm(p_dict)
						pubEditForm.append(wl)
					pubInfoForm = zip(pubEditForm, pubDataCounter)
				publicationaddForm = profile_publications_add_editForm()

				#patentForm populate and edit
				patData = patent.objects.filter(user_id = User_obj)
				if len(patData) == 0:
					patData = 'unavailable'
					patInfoForm = None
				else:
					copy_patData = patData
					patDataCounter = range(len(copy_patData))
					patData = zip(copy_patData, patDataCounter)
					patEditForm = []
					for pa in copy_patData:
						pa_dict = {
							'tuple_id': pa.id,
							'year': pa.year,
							'mode': pa.mode,					
							'status': pa.patent_status,				
							'details': pa.patent_details
						}			
						wl = profile_patent_add_editForm(pa_dict)
						patEditForm.append(wl)
					patInfoForm = zip(patEditForm, patDataCounter)
				patentaddForm = profile_patent_add_editForm()

				skillsData = skills.objects.filter(user_id = User_obj)
				if len(skillsData) == 0:
					skillsData = 'unavailable'
					skillsInfoForm = None
				else:
					counter = 1
					skill_name_text = ''
					for s in skillsData:
						if counter == 1:
							skill_name_text = s.skill_name
						else:
							skill_name_text = skill_name_text + ',' + s.skill_name
						counter = counter + 1

					s_dict = {
						'skill': skill_name_text
					}
					skillsInfoForm = profile_skills_add_editForm(s_dict)
				skillsaddForm = profile_skills_add_editForm()

				variables = RequestContext(request, {
					'workForm': workForm,
					'educationForm': educationForm,
					'certificationForm': certificationForm,
					'publicationForm': publicationForm,
					'extracurricularForm': extracurricularForm,
					'patentForm': patentForm,
					'achievementForm': achievementForm,
					'aboutForm': aboutForm,
					'educationaddForm': educationaddForm,
					'workaddForm': workaddForm,
					'extracurricularaddForm': extracurricularaddForm,
					'certificationaddForm': certificationaddForm,
					'achievementsaddForm': achievementsaddForm,
					'publicationaddForm': publicationaddForm,
					'patentaddForm': patentaddForm,
					'aboutData': aboutData_existing,
					'educationData': educationData,	
					'educationInfoForm': educationInfoForm,
					'workData': workData,
					'workInfoForm': workInfoForm,
					'certificationData': certificationData,
					'certificationInfoForm': certificationInfoForm,
					'exData': exData,
					'exInfoForm': exInfoForm,
					'achData': achData,
					'achInfoForm': achInfoForm,
					'pubData': pubData,
					'pubInfoForm': pubInfoForm,
					'patData': patData,
					'patInfoForm': patInfoForm,
					'skillsaddForm': skillsaddForm,
					'skillsData': skillsData,
					'skillsInfoForm': skillsInfoForm,
					't_educationData': t_educationData,
					't_workData': t_workData,
					't_certificationData': t_certificationData,
					't_extracurricularData': t_extracurricularData,
					't_achievementData': t_achievementData,
					't_publicationData': t_publicationData,
					't_patentData': t_patentData
				})
				return render_to_response('profile-page.html', variables)

			elif work_type == 'Job':
				row_id = workaddForm.cleaned_data['tuple_id']
				# from_date = workaddForm.cleaned_data['job_from_date']
				# to_date = workaddForm.cleaned_data['job_to_date']
				# company_name = workaddForm.cleaned_data['job_company_name']
				# designation = workaddForm.cleaned_data['job_designation']

				# formatted_from_date = from_date[6:] +'-'+ from_date[0:2] +'-'+ from_date[3:5]
				# formatted_to_date = to_date[6:] +'-'+ to_date[0:2] +'-'+ to_date[3:5]
				work_obj = work.objects.get(id = row_id)
				work_obj.delete()
				status = {
					'error': False,
					'error_message': '',
					'success': True,
					'success_message': 'Work details deleted.',
				}
				workForm = profile_workForm()
				educationForm = profile_educationForm()
				certificationForm = profile_certificationForm()
				publicationForm = profile_publicationForm()
				extracurricularForm = profile_extracurricularForm()
				patentForm = profile_patentForm()
				achievementForm = profile_achievementForm()
				t_educationData = education.objects.filter(user_id = User_obj)
				if len(t_educationData) == 0:
					t_educationData = 'unavailable'
				else:
					t_educationData = zip(t_educationData, range(len(t_educationData)))
				t_workData = work.objects.filter(user_id = User_obj)
				if len(t_workData) == 0:
					t_workData = 'unavailable'
				else:
					t_workData = zip(t_workData, range(len(t_workData)))
				t_certificationData = certification.objects.filter(user_id = User_obj)
				if len(t_certificationData) == 0:
					t_certificationData = 'unavailable'
				else:
					t_certificationData = zip(t_certificationData, range(len(t_certificationData)))
				t_extracurricularData = extracurricular_activities.objects.filter(user_id = User_obj)
				if len(t_extracurricularData) == 0:
					t_extracurricularData = 'unavailable'
				else:
					t_extracurricularData = zip(t_extracurricularData, range(len(t_extracurricularData)))
				t_achievementData = achievements.objects.filter(user_id = User_obj)
				if len(t_achievementData) == 0:
					t_achievementData = 'unavailable'
				else:
					t_achievementData = zip(t_achievementData, range(len(t_achievementData)))
				t_publicationData = publication.objects.filter(user_id = User_obj)
				if len(t_publicationData) == 0:
					t_publicationData = 'unavailable'
				else:
					t_publicationData = zip(t_publicationData, range(len(t_publicationData)))
				t_patentData = patent.objects.filter(user_id = User_obj)					
				if len(t_patentData) == 0:
					t_patentData = 'unavailable'
				else:
					t_patentData = zip(t_patentData, range(len(t_patentData)))


				
				# aboutForm population
				try:
					existing_about = user_details.objects.get(user_id = User_obj)
				except:
					existing_about = 'unavailable'
				if existing_about!='unavailable':
					aboutForm_existing = {
						'profession': existing_about.profession,
						'first_name': existing_about.first_name,
						'last_name': existing_about.last_name,
						'dob': existing_about.dob,
						'short_bio': existing_about.short_bio,
						'facebook_url': existing_about.facebook_url,
						'twitter_handle': existing_about.twitter_handle,
						'linkedin_url': existing_about.linkedin_url
					}
				else:
					aboutForm_existing = None
				aboutData_existing = aboutForm_existing
				aboutForm = profile_aboutmeForm(aboutForm_existing)

				#educationForm population and edit
				educationData = education.objects.filter(user_id = User_obj)
				if len(educationData) == 0:
					educationData = 'unavailable'
					educationInfoForm = None
				else:
					copy_educationData = educationData
					educationDataCounter = range(len(copy_educationData))
					educationData = zip(copy_educationData, educationDataCounter)
					educationEditForm = []
					for e in copy_educationData:
						e_dict = {
							'tuple_id': e.id,
							'year': e.year,
							'education_type': e.education_type,
							'institution': e.institution_name,
							'aggregate': e.aggregate,
							'what_did_you_do_there': e.what_did_you_do_there
						}
						el = profile_education_add_editForm(e_dict)
						educationEditForm.append(el)
					educationInfoForm = zip(educationEditForm, educationDataCounter)
				educationaddForm = profile_education_add_editForm()

				#workForm population and edit
				workData = work.objects.filter(user_id = User_obj)
				if len(workData) == 0:
					workData = 'unavailable'
					workInfoForm = None
				else:
					copy_workData = workData
					workDataCounter = range(len(copy_workData))
					workData = zip(copy_workData, workDataCounter)
					workEditForm = []
					for w in copy_workData:
						if w.work_type == 'Internship':
							w_dict = {
								'tuple_id': w.id,
								'work_type': w.work_type,
								'internship_company_name': w.internship_company_name,
								'internship_from_date': w.internship_date_from,
								'internship_to_date': w.internship_date_to,
								'internship_title': w.internship_title
							}
						elif w.work_type == 'Job':
							w_dict = {
								'tuple_id': w.id,
								'work_type': w.work_type,
								'job_company_name': w.job_company_name,
								'job_designation': w.job_designation,
								'job_from_date': w.job_date_from,
								'job_to_date': w.job_date_to
							}
						else:
							w_dict = {
								'tuple_id': w.id,
								'work_type': w.work_type,
								'freelancer_client': w.freelancer_client_name,
								'freelancer_project_title': w.freelancer_project_title,
								'freelancer_link': w.freelancer_link,
								'freelancer_project_status': w.freelancer_status,
								'freelancer_year': w.freelancer_year
							}
						wl = profile_work_add_editForm(w_dict)
						workEditForm.append(wl)
					workInfoForm = zip(workEditForm, workDataCounter)
				workaddForm = profile_work_add_editForm()

				#certificationForm populate and edit
				certificationData = certification.objects.filter(user_id = User_obj)
				if len(certificationData) == 0:
					certificationData = 'unavailable'
					certificationInfoForm = None
				else:
					copy_certificationData = certificationData
					certificationDataCounter = range(len(copy_certificationData))
					certificationData = zip(copy_certificationData, certificationDataCounter)
					certificationEditForm = []
					for c in copy_certificationData:
						c_dict = {
							'tuple_id': c.id,
							'year': c.year,
							'agency': c.agency,
							'mode': c.mode_of_certification,
							'details': c.details,					
						}		
						wl = profile_certification_add_editForm(c_dict)
						certificationEditForm.append(wl)
					certificationInfoForm = zip(certificationEditForm, certificationDataCounter)
				certificationaddForm = profile_certification_add_editForm()

				#extracurricularForm populate and edit
				exData = extracurricular_activities.objects.filter(user_id = User_obj)
				if len(exData) == 0:
					exData = 'unavailable'
					exInfoForm = None
				else:
					copy_exData = exData
					exDataCounter = range(len(copy_exData))
					exData = zip(copy_exData, exDataCounter)
					exEditForm = []
					for e in copy_exData:
						e_dict = {
							'tuple_id': e.id,
							'year': e.year,
							'activity_type': e.activity_type,
							'title': e.title,
							'details': e.activity_details,
							'organization': e.organization,
							'link': e.link					
						}			
						wl = profile_extracurricular_add_editForm(e_dict)
						exEditForm.append(wl)
					exInfoForm = zip(exEditForm, exDataCounter)
				extracurricularaddForm = profile_extracurricular_add_editForm()

				#achievementForm populate and edit
				achData = achievements.objects.filter(user_id = User_obj)
				if len(achData) == 0:
					achData = 'unavailable'
					achInfoForm = None
				else:
					copy_achData = achData
					achDataCounter = range(len(copy_achData))
					achData = zip(copy_achData, achDataCounter)
					achEditForm = []
					for a in copy_achData:
						a_dict = {
							'tuple_id': a.id,
							'year': a.year,
							'achievement_type': a.achievement_type,
							'title': a.title,
							'details': a.details,
							'organization': a.organization,
							'link': a.link					
						}			
						wl = profile_achievements_add_editForm(a_dict)
						achEditForm.append(wl)
					achInfoForm = zip(achEditForm, achDataCounter)
				achievementsaddForm = profile_achievements_add_editForm()

				#publicationForm populate and edit
				pubData = publication.objects.filter(user_id = User_obj)
				if len(pubData) == 0:
					pubData = 'unavailable'
					pubInfoForm = None
				else:
					copy_pubData = pubData
					pubDataCounter = range(len(copy_pubData))
					pubData = zip(copy_pubData, pubDataCounter)
					pubEditForm = []
					for p in copy_pubData:
						p_dict = {
							'tuple_id': p.id,
							'year': p.year,
							'mode': p.mode,
							'journal': p.journal,
							'status': p.status,				
							'details': p.details,					
							'link': p.link					
						}			
						wl = profile_publications_add_editForm(p_dict)
						pubEditForm.append(wl)
					pubInfoForm = zip(pubEditForm, pubDataCounter)
				publicationaddForm = profile_publications_add_editForm()

				#patentForm populate and edit
				patData = patent.objects.filter(user_id = User_obj)
				if len(patData) == 0:
					patData = 'unavailable'
					patInfoForm = None
				else:
					copy_patData = patData
					patDataCounter = range(len(copy_patData))
					patData = zip(copy_patData, patDataCounter)
					patEditForm = []
					for pa in copy_patData:
						pa_dict = {
							'tuple_id': pa.id,
							'year': pa.year,
							'mode': pa.mode,					
							'status': pa.patent_status,				
							'details': pa.patent_details
						}			
						wl = profile_patent_add_editForm(pa_dict)
						patEditForm.append(wl)
					patInfoForm = zip(patEditForm, patDataCounter)
				patentaddForm = profile_patent_add_editForm()

				skillsData = skills.objects.filter(user_id = User_obj)
				if len(skillsData) == 0:
					skillsData = 'unavailable'
					skillsInfoForm = None
				else:
					counter = 1
					skill_name_text = ''
					for s in skillsData:
						if counter == 1:
							skill_name_text = s.skill_name
						else:
							skill_name_text = skill_name_text + ',' + s.skill_name
						counter = counter + 1

					s_dict = {
						'skill': skill_name_text
					}
					skillsInfoForm = profile_skills_add_editForm(s_dict)
				skillsaddForm = profile_skills_add_editForm()

				variables = RequestContext(request, {
					'workForm': workForm,
					'educationForm': educationForm,
					'certificationForm': certificationForm,
					'publicationForm': publicationForm,
					'extracurricularForm': extracurricularForm,
					'patentForm': patentForm,
					'achievementForm': achievementForm,
					'aboutForm': aboutForm,
					'educationaddForm': educationaddForm,
					'workaddForm': workaddForm,
					'extracurricularaddForm': extracurricularaddForm,
					'certificationaddForm': certificationaddForm,
					'achievementsaddForm': achievementsaddForm,
					'publicationaddForm': publicationaddForm,
					'patentaddForm': patentaddForm,
					'aboutData': aboutData_existing,
					'educationData': educationData,	
					'educationInfoForm': educationInfoForm,
					'workData': workData,
					'workInfoForm': workInfoForm,
					'certificationData': certificationData,
					'certificationInfoForm': certificationInfoForm,
					'exData': exData,
					'exInfoForm': exInfoForm,
					'achData': achData,
					'achInfoForm': achInfoForm,
					'pubData': pubData,
					'pubInfoForm': pubInfoForm,
					'patData': patData,
					'patInfoForm': patInfoForm,
					'skillsaddForm': skillsaddForm,
					'skillsData': skillsData,
					'skillsInfoForm': skillsInfoForm,
					't_educationData': t_educationData,
					't_workData': t_workData,
					't_certificationData': t_certificationData,
					't_extracurricularData': t_extracurricularData,
					't_achievementData': t_achievementData,
					't_publicationData': t_publicationData,
					't_patentData': t_patentData
				})
				return render_to_response('profile-page.html', variables)

			else:
				row_id = workaddForm.cleaned_data['tuple_id']
				# client = workaddForm.cleaned_data['freelancer_client']
				# title = workaddForm.cleaned_data['freelancer_project_title']
				# status = workaddForm.cleaned_data['freelancer_project_status']
				# link = workaddForm.cleaned_data['freelancer_link']		
				work_obj = work.objects.get(id = row_id)
				work_obj.delete()

				status = {
					'error': False,
					'error_message': '',
					'success': True,
					'success_message': 'Work details deleted.',
				}
				workForm = profile_workForm()
				educationForm = profile_educationForm()
				certificationForm = profile_certificationForm()
				publicationForm = profile_publicationForm()
				extracurricularForm = profile_extracurricularForm()
				patentForm = profile_patentForm()
				achievementForm = profile_achievementForm()
				t_educationData = education.objects.filter(user_id = User_obj)
				if len(t_educationData) == 0:
					t_educationData = 'unavailable'
				else:
					t_educationData = zip(t_educationData, range(len(t_educationData)))
				t_workData = work.objects.filter(user_id = User_obj)
				if len(t_workData) == 0:
					t_workData = 'unavailable'
				else:
					t_workData = zip(t_workData, range(len(t_workData)))
				t_certificationData = certification.objects.filter(user_id = User_obj)
				if len(t_certificationData) == 0:
					t_certificationData = 'unavailable'
				else:
					t_certificationData = zip(t_certificationData, range(len(t_certificationData)))
				t_extracurricularData = extracurricular_activities.objects.filter(user_id = User_obj)
				if len(t_extracurricularData) == 0:
					t_extracurricularData = 'unavailable'
				else:
					t_extracurricularData = zip(t_extracurricularData, range(len(t_extracurricularData)))
				t_achievementData = achievements.objects.filter(user_id = User_obj)
				if len(t_achievementData) == 0:
					t_achievementData = 'unavailable'
				else:
					t_achievementData = zip(t_achievementData, range(len(t_achievementData)))
				t_publicationData = publication.objects.filter(user_id = User_obj)
				if len(t_publicationData) == 0:
					t_publicationData = 'unavailable'
				else:
					t_publicationData = zip(t_publicationData, range(len(t_publicationData)))
				t_patentData = patent.objects.filter(user_id = User_obj)					
				if len(t_patentData) == 0:
					t_patentData = 'unavailable'
				else:
					t_patentData = zip(t_patentData, range(len(t_patentData)))


				
				# aboutForm population
				try:
					existing_about = user_details.objects.get(user_id = User_obj)
				except:
					existing_about = 'unavailable'
				if existing_about!='unavailable':
					aboutForm_existing = {
						'profession': existing_about.profession,
						'first_name': existing_about.first_name,
						'last_name': existing_about.last_name,
						'dob': existing_about.dob,
						'short_bio': existing_about.short_bio,
						'facebook_url': existing_about.facebook_url,
						'twitter_handle': existing_about.twitter_handle,
						'linkedin_url': existing_about.linkedin_url
					}
				else:
					aboutForm_existing = None
				aboutData_existing = aboutForm_existing
				aboutForm = profile_aboutmeForm(aboutForm_existing)

				#educationForm population and edit
				educationData = education.objects.filter(user_id = User_obj)
				if len(educationData) == 0:
					educationData = 'unavailable'
					educationInfoForm = None
				else:
					copy_educationData = educationData
					educationDataCounter = range(len(copy_educationData))
					educationData = zip(copy_educationData, educationDataCounter)
					educationEditForm = []
					for e in copy_educationData:
						e_dict = {
							'tuple_id': e.id,
							'year': e.year,
							'education_type': e.education_type,
							'institution': e.institution_name,
							'aggregate': e.aggregate,
							'what_did_you_do_there': e.what_did_you_do_there
						}
						el = profile_education_add_editForm(e_dict)
						educationEditForm.append(el)
					educationInfoForm = zip(educationEditForm, educationDataCounter)
				educationaddForm = profile_education_add_editForm()

				#workForm population and edit
				workData = work.objects.filter(user_id = User_obj)
				if len(workData) == 0:
					workData = 'unavailable'
					workInfoForm = None
				else:
					copy_workData = workData
					workDataCounter = range(len(copy_workData))
					workData = zip(copy_workData, workDataCounter)
					workEditForm = []
					for w in copy_workData:
						if w.work_type == 'Internship':
							w_dict = {
								'tuple_id': w.id,
								'work_type': w.work_type,
								'internship_company_name': w.internship_company_name,
								'internship_from_date': w.internship_date_from,
								'internship_to_date': w.internship_date_to,
								'internship_title': w.internship_title
							}
						elif w.work_type == 'Job':
							w_dict = {
								'tuple_id': w.id,
								'work_type': w.work_type,
								'job_company_name': w.job_company_name,
								'job_designation': w.job_designation,
								'job_from_date': w.job_date_from,
								'job_to_date': w.job_date_to
							}
						else:
							w_dict = {
								'tuple_id': w.id,
								'work_type': w.work_type,
								'freelancer_client': w.freelancer_client_name,
								'freelancer_project_title': w.freelancer_project_title,
								'freelancer_link': w.freelancer_link,
								'freelancer_project_status': w.freelancer_status,
								'freelancer_year': w.freelancer_year
							}
						wl = profile_work_add_editForm(w_dict)
						workEditForm.append(wl)
					workInfoForm = zip(workEditForm, workDataCounter)
				workaddForm = profile_work_add_editForm()

				#certificationForm populate and edit
				certificationData = certification.objects.filter(user_id = User_obj)
				if len(certificationData) == 0:
					certificationData = 'unavailable'
					certificationInfoForm = None
				else:
					copy_certificationData = certificationData
					certificationDataCounter = range(len(copy_certificationData))
					certificationData = zip(copy_certificationData, certificationDataCounter)
					certificationEditForm = []
					for c in copy_certificationData:
						c_dict = {
							'tuple_id': c.id,
							'year': c.year,
							'agency': c.agency,
							'mode': c.mode_of_certification,
							'details': c.details,					
						}		
						wl = profile_certification_add_editForm(c_dict)
						certificationEditForm.append(wl)
					certificationInfoForm = zip(certificationEditForm, certificationDataCounter)
				certificationaddForm = profile_certification_add_editForm()

				#extracurricularForm populate and edit
				exData = extracurricular_activities.objects.filter(user_id = User_obj)
				if len(exData) == 0:
					exData = 'unavailable'
					exInfoForm = None
				else:
					copy_exData = exData
					exDataCounter = range(len(copy_exData))
					exData = zip(copy_exData, exDataCounter)
					exEditForm = []
					for e in copy_exData:
						e_dict = {
							'tuple_id': e.id,
							'year': e.year,
							'activity_type': e.activity_type,
							'title': e.title,
							'details': e.activity_details,
							'organization': e.organization,
							'link': e.link					
						}			
						wl = profile_extracurricular_add_editForm(e_dict)
						exEditForm.append(wl)
					exInfoForm = zip(exEditForm, exDataCounter)
				extracurricularaddForm = profile_extracurricular_add_editForm()

				#achievementForm populate and edit
				achData = achievements.objects.filter(user_id = User_obj)
				if len(achData) == 0:
					achData = 'unavailable'
					achInfoForm = None
				else:
					copy_achData = achData
					achDataCounter = range(len(copy_achData))
					achData = zip(copy_achData, achDataCounter)
					achEditForm = []
					for a in copy_achData:
						a_dict = {
							'tuple_id': a.id,
							'year': a.year,
							'achievement_type': a.achievement_type,
							'title': a.title,
							'details': a.details,
							'organization': a.organization,
							'link': a.link					
						}			
						wl = profile_achievements_add_editForm(a_dict)
						achEditForm.append(wl)
					achInfoForm = zip(achEditForm, achDataCounter)
				achievementsaddForm = profile_achievements_add_editForm()

				#publicationForm populate and edit
				pubData = publication.objects.filter(user_id = User_obj)
				if len(pubData) == 0:
					pubData = 'unavailable'
					pubInfoForm = None
				else:
					copy_pubData = pubData
					pubDataCounter = range(len(copy_pubData))
					pubData = zip(copy_pubData, pubDataCounter)
					pubEditForm = []
					for p in copy_pubData:
						p_dict = {
							'tuple_id': p.id,
							'year': p.year,
							'mode': p.mode,
							'journal': p.journal,
							'status': p.status,				
							'details': p.details,					
							'link': p.link					
						}			
						wl = profile_publications_add_editForm(p_dict)
						pubEditForm.append(wl)
					pubInfoForm = zip(pubEditForm, pubDataCounter)
				publicationaddForm = profile_publications_add_editForm()

				#patentForm populate and edit
				patData = patent.objects.filter(user_id = User_obj)
				if len(patData) == 0:
					patData = 'unavailable'
					patInfoForm = None
				else:
					copy_patData = patData
					patDataCounter = range(len(copy_patData))
					patData = zip(copy_patData, patDataCounter)
					patEditForm = []
					for pa in copy_patData:
						pa_dict = {
							'tuple_id': pa.id,
							'year': pa.year,
							'mode': pa.mode,					
							'status': pa.patent_status,				
							'details': pa.patent_details
						}			
						wl = profile_patent_add_editForm(pa_dict)
						patEditForm.append(wl)
					patInfoForm = zip(patEditForm, patDataCounter)
				patentaddForm = profile_patent_add_editForm()

				skillsData = skills.objects.filter(user_id = User_obj)
				if len(skillsData) == 0:
					skillsData = 'unavailable'
					skillsInfoForm = None
				else:
					counter = 1
					skill_name_text = ''
					for s in skillsData:
						if counter == 1:
							skill_name_text = s.skill_name
						else:
							skill_name_text = skill_name_text + ',' + s.skill_name
						counter = counter + 1

					s_dict = {
						'skill': skill_name_text
					}
					skillsInfoForm = profile_skills_add_editForm(s_dict)
				skillsaddForm = profile_skills_add_editForm()

				variables = RequestContext(request, {
					'workForm': workForm,
					'educationForm': educationForm,
					'certificationForm': certificationForm,
					'publicationForm': publicationForm,
					'extracurricularForm': extracurricularForm,
					'patentForm': patentForm,
					'achievementForm': achievementForm,
					'aboutForm': aboutForm,
					'educationaddForm': educationaddForm,
					'workaddForm': workaddForm,
					'extracurricularaddForm': extracurricularaddForm,
					'certificationaddForm': certificationaddForm,
					'achievementsaddForm': achievementsaddForm,
					'publicationaddForm': publicationaddForm,
					'patentaddForm': patentaddForm,
					'aboutData': aboutData_existing,
					'educationData': educationData,	
					'educationInfoForm': educationInfoForm,
					'workData': workData,
					'workInfoForm': workInfoForm,
					'certificationData': certificationData,
					'certificationInfoForm': certificationInfoForm,
					'exData': exData,
					'exInfoForm': exInfoForm,
					'achData': achData,
					'achInfoForm': achInfoForm,
					'pubData': pubData,
					'pubInfoForm': pubInfoForm,
					'patData': patData,
					'patInfoForm': patInfoForm,
					'skillsaddForm': skillsaddForm,
					'skillsData': skillsData,
					'skillsInfoForm': skillsInfoForm,
					't_educationData': t_educationData,
					't_workData': t_workData,
					't_certificationData': t_certificationData,
					't_extracurricularData': t_extracurricularData,
					't_achievementData': t_achievementData,
					't_publicationData': t_publicationData,
					't_patentData': t_patentData
				})
				return render_to_response('profile-page.html', variables)

	elif request.method=='GET' and 'workaddForm' in request.GET:
		workaddForm = profile_work_add_editForm(request.GET)
		if workaddForm.is_valid():
			work_type = workaddForm.cleaned_data['work_type']
			if work_type == 'Internship':
				company_name = workaddForm.cleaned_data['internship_company_name']
				from_date = workaddForm.cleaned_data['internship_from_date']
				to_date = workaddForm.cleaned_data['internship_to_date']
				title = workaddForm.cleaned_data['internship_title']

				formatted_from_date = from_date[6:] +'-'+ from_date[0:2] +'-'+ from_date[3:5]
				formatted_to_date = to_date[6:] +'-'+ to_date[0:2] +'-'+ to_date[3:5]

				work_obj = work(
					user_id = User_obj,
					work_type = work_type,
					internship_company_name = company_name,
					internship_date_from = formatted_from_date,
					internship_date_to = formatted_to_date,
					internship_title = title,
				)
				work_obj.save()
				status = {
					'error': False,
					'error_message': '',
					'success': True,
					'success_message': 'Work details saved.',
				}
				workForm = profile_workForm()
				educationForm = profile_educationForm()
				certificationForm = profile_certificationForm()
				publicationForm = profile_publicationForm()
				extracurricularForm = profile_extracurricularForm()
				patentForm = profile_patentForm()
				achievementForm = profile_achievementForm()
				t_educationData = education.objects.filter(user_id = User_obj)
				if len(t_educationData) == 0:
					t_educationData = 'unavailable'
				else:
					t_educationData = zip(t_educationData, range(len(t_educationData)))
				t_workData = work.objects.filter(user_id = User_obj)
				if len(t_workData) == 0:
					t_workData = 'unavailable'
				else:
					t_workData = zip(t_workData, range(len(t_workData)))
				t_certificationData = certification.objects.filter(user_id = User_obj)
				if len(t_certificationData) == 0:
					t_certificationData = 'unavailable'
				else:
					t_certificationData = zip(t_certificationData, range(len(t_certificationData)))
				t_extracurricularData = extracurricular_activities.objects.filter(user_id = User_obj)
				if len(t_extracurricularData) == 0:
					t_extracurricularData = 'unavailable'
				else:
					t_extracurricularData = zip(t_extracurricularData, range(len(t_extracurricularData)))
				t_achievementData = achievements.objects.filter(user_id = User_obj)
				if len(t_achievementData) == 0:
					t_achievementData = 'unavailable'
				else:
					t_achievementData = zip(t_achievementData, range(len(t_achievementData)))
				t_publicationData = publication.objects.filter(user_id = User_obj)
				if len(t_publicationData) == 0:
					t_publicationData = 'unavailable'
				else:
					t_publicationData = zip(t_publicationData, range(len(t_publicationData)))
				t_patentData = patent.objects.filter(user_id = User_obj)					
				if len(t_patentData) == 0:
					t_patentData = 'unavailable'
				else:
					t_patentData = zip(t_patentData, range(len(t_patentData)))


				
				# aboutForm population
				try:
					existing_about = user_details.objects.get(user_id = User_obj)
				except:
					existing_about = 'unavailable'
				if existing_about!='unavailable':
					aboutForm_existing = {
						'profession': existing_about.profession,
						'first_name': existing_about.first_name,
						'last_name': existing_about.last_name,
						'dob': existing_about.dob,
						'short_bio': existing_about.short_bio,
						'facebook_url': existing_about.facebook_url,
						'twitter_handle': existing_about.twitter_handle,
						'linkedin_url': existing_about.linkedin_url
					}
				else:
					aboutForm_existing = None
				aboutData_existing = aboutForm_existing
				aboutForm = profile_aboutmeForm(aboutForm_existing)

				#educationForm population and edit
				educationData = education.objects.filter(user_id = User_obj)
				if len(educationData) == 0:
					educationData = 'unavailable'
					educationInfoForm = None
				else:
					copy_educationData = educationData
					educationDataCounter = range(len(copy_educationData))
					educationData = zip(copy_educationData, educationDataCounter)
					educationEditForm = []
					for e in copy_educationData:
						e_dict = {
							'tuple_id': e.id,
							'year': e.year,
							'education_type': e.education_type,
							'institution': e.institution_name,
							'aggregate': e.aggregate,
							'what_did_you_do_there': e.what_did_you_do_there
						}
						el = profile_education_add_editForm(e_dict)
						educationEditForm.append(el)
					educationInfoForm = zip(educationEditForm, educationDataCounter)
				educationaddForm = profile_education_add_editForm()

				#workForm population and edit
				workData = work.objects.filter(user_id = User_obj)
				if len(workData) == 0:
					workData = 'unavailable'
					workInfoForm = None
				else:
					copy_workData = workData
					workDataCounter = range(len(copy_workData))
					workData = zip(copy_workData, workDataCounter)
					workEditForm = []
					for w in copy_workData:
						if w.work_type == 'Internship':
							w_dict = {
								'tuple_id': w.id,
								'work_type': w.work_type,
								'internship_company_name': w.internship_company_name,
								'internship_from_date': w.internship_date_from,
								'internship_to_date': w.internship_date_to,
								'internship_title': w.internship_title
							}
						elif w.work_type == 'Job':
							w_dict = {
								'tuple_id': w.id,
								'work_type': w.work_type,
								'job_company_name': w.job_company_name,
								'job_designation': w.job_designation,
								'job_from_date': w.job_date_from,
								'job_to_date': w.job_date_to
							}
						else:
							w_dict = {
								'tuple_id': w.id,
								'work_type': w.work_type,
								'freelancer_client': w.freelancer_client_name,
								'freelancer_project_title': w.freelancer_project_title,
								'freelancer_link': w.freelancer_link,
								'freelancer_project_status': w.freelancer_status,
								'freelancer_year': w.freelancer_year
							}
						wl = profile_work_add_editForm(w_dict)
						workEditForm.append(wl)
					workInfoForm = zip(workEditForm, workDataCounter)
				workaddForm = profile_work_add_editForm()

				#certificationForm populate and edit
				certificationData = certification.objects.filter(user_id = User_obj)
				if len(certificationData) == 0:
					certificationData = 'unavailable'
					certificationInfoForm = None
				else:
					copy_certificationData = certificationData
					certificationDataCounter = range(len(copy_certificationData))
					certificationData = zip(copy_certificationData, certificationDataCounter)
					certificationEditForm = []
					for c in copy_certificationData:
						c_dict = {
							'tuple_id': c.id,
							'year': c.year,
							'agency': c.agency,
							'mode': c.mode_of_certification,
							'details': c.details,					
						}		
						wl = profile_certification_add_editForm(c_dict)
						certificationEditForm.append(wl)
					certificationInfoForm = zip(certificationEditForm, certificationDataCounter)
				certificationaddForm = profile_certification_add_editForm()

				#extracurricularForm populate and edit
				exData = extracurricular_activities.objects.filter(user_id = User_obj)
				if len(exData) == 0:
					exData = 'unavailable'
					exInfoForm = None
				else:
					copy_exData = exData
					exDataCounter = range(len(copy_exData))
					exData = zip(copy_exData, exDataCounter)
					exEditForm = []
					for e in copy_exData:
						e_dict = {
							'tuple_id': e.id,
							'year': e.year,
							'activity_type': e.activity_type,
							'title': e.title,
							'details': e.activity_details,
							'organization': e.organization,
							'link': e.link					
						}			
						wl = profile_extracurricular_add_editForm(e_dict)
						exEditForm.append(wl)
					exInfoForm = zip(exEditForm, exDataCounter)
				extracurricularaddForm = profile_extracurricular_add_editForm()

				#achievementForm populate and edit
				achData = achievements.objects.filter(user_id = User_obj)
				if len(achData) == 0:
					achData = 'unavailable'
					achInfoForm = None
				else:
					copy_achData = achData
					achDataCounter = range(len(copy_achData))
					achData = zip(copy_achData, achDataCounter)
					achEditForm = []
					for a in copy_achData:
						a_dict = {
							'tuple_id': a.id,
							'year': a.year,
							'achievement_type': a.achievement_type,
							'title': a.title,
							'details': a.details,
							'organization': a.organization,
							'link': a.link					
						}			
						wl = profile_achievements_add_editForm(a_dict)
						achEditForm.append(wl)
					achInfoForm = zip(achEditForm, achDataCounter)
				achievementsaddForm = profile_achievements_add_editForm()

				#publicationForm populate and edit
				pubData = publication.objects.filter(user_id = User_obj)
				if len(pubData) == 0:
					pubData = 'unavailable'
					pubInfoForm = None
				else:
					copy_pubData = pubData
					pubDataCounter = range(len(copy_pubData))
					pubData = zip(copy_pubData, pubDataCounter)
					pubEditForm = []
					for p in copy_pubData:
						p_dict = {
							'tuple_id': p.id,
							'year': p.year,
							'mode': p.mode,
							'journal': p.journal,
							'status': p.status,				
							'details': p.details,					
							'link': p.link					
						}			
						wl = profile_publications_add_editForm(p_dict)
						pubEditForm.append(wl)
					pubInfoForm = zip(pubEditForm, pubDataCounter)
				publicationaddForm = profile_publications_add_editForm()

				#patentForm populate and edit
				patData = patent.objects.filter(user_id = User_obj)
				if len(patData) == 0:
					patData = 'unavailable'
					patInfoForm = None
				else:
					copy_patData = patData
					patDataCounter = range(len(copy_patData))
					patData = zip(copy_patData, patDataCounter)
					patEditForm = []
					for pa in copy_patData:
						pa_dict = {
							'tuple_id': pa.id,
							'year': pa.year,
							'mode': pa.mode,					
							'status': pa.patent_status,				
							'details': pa.patent_details
						}			
						wl = profile_patent_add_editForm(pa_dict)
						patEditForm.append(wl)
					patInfoForm = zip(patEditForm, patDataCounter)
				patentaddForm = profile_patent_add_editForm()

				skillsData = skills.objects.filter(user_id = User_obj)
				if len(skillsData) == 0:
					skillsData = 'unavailable'
					skillsInfoForm = None
				else:
					counter = 1
					skill_name_text = ''
					for s in skillsData:
						if counter == 1:
							skill_name_text = s.skill_name
						else:
							skill_name_text = skill_name_text + ',' + s.skill_name
						counter = counter + 1

					s_dict = {
						'skill': skill_name_text
					}
					skillsInfoForm = profile_skills_add_editForm(s_dict)
				skillsaddForm = profile_skills_add_editForm()

				variables = RequestContext(request, {
					'workForm': workForm,
					'educationForm': educationForm,
					'certificationForm': certificationForm,
					'publicationForm': publicationForm,
					'extracurricularForm': extracurricularForm,
					'patentForm': patentForm,
					'achievementForm': achievementForm,
					'aboutForm': aboutForm,
					'educationaddForm': educationaddForm,
					'workaddForm': workaddForm,
					'extracurricularaddForm': extracurricularaddForm,
					'certificationaddForm': certificationaddForm,
					'achievementsaddForm': achievementsaddForm,
					'publicationaddForm': publicationaddForm,
					'patentaddForm': patentaddForm,
					'aboutData': aboutData_existing,
					'educationData': educationData,	
					'educationInfoForm': educationInfoForm,
					'workData': workData,
					'workInfoForm': workInfoForm,
					'certificationData': certificationData,
					'certificationInfoForm': certificationInfoForm,
					'exData': exData,
					'exInfoForm': exInfoForm,
					'achData': achData,
					'achInfoForm': achInfoForm,
					'pubData': pubData,
					'pubInfoForm': pubInfoForm,
					'patData': patData,
					'patInfoForm': patInfoForm,
					'skillsaddForm': skillsaddForm,
					'skillsData': skillsData,
					'skillsInfoForm': skillsInfoForm,
					't_educationData': t_educationData,
					't_workData': t_workData,
					't_certificationData': t_certificationData,
					't_extracurricularData': t_extracurricularData,
					't_achievementData': t_achievementData,
					't_publicationData': t_publicationData,
					't_patentData': t_patentData
				})
				return render_to_response('profile-page.html', variables)

			elif work_type == 'Job':
				from_date = workaddForm.cleaned_data['job_from_date']
				to_date = workaddForm.cleaned_data['job_to_date']
				company_name = workaddForm.cleaned_data['job_company_name']
				designation = workaddForm.cleaned_data['job_designation']

				formatted_from_date = from_date[6:] +'-'+ from_date[0:2] +'-'+ from_date[3:5]
				formatted_to_date = to_date[6:] +'-'+ to_date[0:2] +'-'+ to_date[3:5]

				work_obj = work(
					user_id = User_obj,
					work_type = work_type,
					job_date_from = formatted_from_date,
					job_date_to = formatted_to_date,
					job_company_name = company_name,
					job_designation = designation
				)
				work_obj.save()
				status = {
					'error': False,
					'error_message': '',
					'success': True,
					'success_message': 'Work details saved.',
				}
				workForm = profile_workForm()
				educationForm = profile_educationForm()
				certificationForm = profile_certificationForm()
				publicationForm = profile_publicationForm()
				extracurricularForm = profile_extracurricularForm()
				patentForm = profile_patentForm()
				achievementForm = profile_achievementForm()
				t_educationData = education.objects.filter(user_id = User_obj)
				if len(t_educationData) == 0:
					t_educationData = 'unavailable'
				else:
					t_educationData = zip(t_educationData, range(len(t_educationData)))
				t_workData = work.objects.filter(user_id = User_obj)
				if len(t_workData) == 0:
					t_workData = 'unavailable'
				else:
					t_workData = zip(t_workData, range(len(t_workData)))
				t_certificationData = certification.objects.filter(user_id = User_obj)
				if len(t_certificationData) == 0:
					t_certificationData = 'unavailable'
				else:
					t_certificationData = zip(t_certificationData, range(len(t_certificationData)))
				t_extracurricularData = extracurricular_activities.objects.filter(user_id = User_obj)
				if len(t_extracurricularData) == 0:
					t_extracurricularData = 'unavailable'
				else:
					t_extracurricularData = zip(t_extracurricularData, range(len(t_extracurricularData)))
				t_achievementData = achievements.objects.filter(user_id = User_obj)
				if len(t_achievementData) == 0:
					t_achievementData = 'unavailable'
				else:
					t_achievementData = zip(t_achievementData, range(len(t_achievementData)))
				t_publicationData = publication.objects.filter(user_id = User_obj)
				if len(t_publicationData) == 0:
					t_publicationData = 'unavailable'
				else:
					t_publicationData = zip(t_publicationData, range(len(t_publicationData)))
				t_patentData = patent.objects.filter(user_id = User_obj)					
				if len(t_patentData) == 0:
					t_patentData = 'unavailable'
				else:
					t_patentData = zip(t_patentData, range(len(t_patentData)))


				
				# aboutForm population
				try:
					existing_about = user_details.objects.get(user_id = User_obj)
				except:
					existing_about = 'unavailable'
				if existing_about!='unavailable':
					aboutForm_existing = {
						'profession': existing_about.profession,
						'first_name': existing_about.first_name,
						'last_name': existing_about.last_name,
						'dob': existing_about.dob,
						'short_bio': existing_about.short_bio,
						'facebook_url': existing_about.facebook_url,
						'twitter_handle': existing_about.twitter_handle,
						'linkedin_url': existing_about.linkedin_url
					}
				else:
					aboutForm_existing = None
				aboutData_existing = aboutForm_existing
				aboutForm = profile_aboutmeForm(aboutForm_existing)

				#educationForm population and edit
				educationData = education.objects.filter(user_id = User_obj)
				if len(educationData) == 0:
					educationData = 'unavailable'
					educationInfoForm = None
				else:
					copy_educationData = educationData
					educationDataCounter = range(len(copy_educationData))
					educationData = zip(copy_educationData, educationDataCounter)
					educationEditForm = []
					for e in copy_educationData:
						e_dict = {
							'tuple_id': e.id,
							'year': e.year,
							'education_type': e.education_type,
							'institution': e.institution_name,
							'aggregate': e.aggregate,
							'what_did_you_do_there': e.what_did_you_do_there
						}
						el = profile_education_add_editForm(e_dict)
						educationEditForm.append(el)
					educationInfoForm = zip(educationEditForm, educationDataCounter)
				educationaddForm = profile_education_add_editForm()

				#workForm population and edit
				workData = work.objects.filter(user_id = User_obj)
				if len(workData) == 0:
					workData = 'unavailable'
					workInfoForm = None
				else:
					copy_workData = workData
					workDataCounter = range(len(copy_workData))
					workData = zip(copy_workData, workDataCounter)
					workEditForm = []
					for w in copy_workData:
						if w.work_type == 'Internship':
							w_dict = {
								'tuple_id': w.id,
								'work_type': w.work_type,
								'internship_company_name': w.internship_company_name,
								'internship_from_date': w.internship_date_from,
								'internship_to_date': w.internship_date_to,
								'internship_title': w.internship_title
							}
						elif w.work_type == 'Job':
							w_dict = {
								'tuple_id': w.id,
								'work_type': w.work_type,
								'job_company_name': w.job_company_name,
								'job_designation': w.job_designation,
								'job_from_date': w.job_date_from,
								'job_to_date': w.job_date_to
							}
						else:
							w_dict = {
								'tuple_id': w.id,
								'work_type': w.work_type,
								'freelancer_client': w.freelancer_client_name,
								'freelancer_project_title': w.freelancer_project_title,
								'freelancer_link': w.freelancer_link,
								'freelancer_project_status': w.freelancer_status,
								'freelancer_year': w.freelancer_year
							}
						wl = profile_work_add_editForm(w_dict)
						workEditForm.append(wl)
					workInfoForm = zip(workEditForm, workDataCounter)
				workaddForm = profile_work_add_editForm()

				#certificationForm populate and edit
				certificationData = certification.objects.filter(user_id = User_obj)
				if len(certificationData) == 0:
					certificationData = 'unavailable'
					certificationInfoForm = None
				else:
					copy_certificationData = certificationData
					certificationDataCounter = range(len(copy_certificationData))
					certificationData = zip(copy_certificationData, certificationDataCounter)
					certificationEditForm = []
					for c in copy_certificationData:
						c_dict = {
							'tuple_id': c.id,
							'year': c.year,
							'agency': c.agency,
							'mode': c.mode_of_certification,
							'details': c.details,					
						}		
						wl = profile_certification_add_editForm(c_dict)
						certificationEditForm.append(wl)
					certificationInfoForm = zip(certificationEditForm, certificationDataCounter)
				certificationaddForm = profile_certification_add_editForm()

				#extracurricularForm populate and edit
				exData = extracurricular_activities.objects.filter(user_id = User_obj)
				if len(exData) == 0:
					exData = 'unavailable'
					exInfoForm = None
				else:
					copy_exData = exData
					exDataCounter = range(len(copy_exData))
					exData = zip(copy_exData, exDataCounter)
					exEditForm = []
					for e in copy_exData:
						e_dict = {
							'tuple_id': e.id,
							'year': e.year,
							'activity_type': e.activity_type,
							'title': e.title,
							'details': e.activity_details,
							'organization': e.organization,
							'link': e.link					
						}			
						wl = profile_extracurricular_add_editForm(e_dict)
						exEditForm.append(wl)
					exInfoForm = zip(exEditForm, exDataCounter)
				extracurricularaddForm = profile_extracurricular_add_editForm()

				#achievementForm populate and edit
				achData = achievements.objects.filter(user_id = User_obj)
				if len(achData) == 0:
					achData = 'unavailable'
					achInfoForm = None
				else:
					copy_achData = achData
					achDataCounter = range(len(copy_achData))
					achData = zip(copy_achData, achDataCounter)
					achEditForm = []
					for a in copy_achData:
						a_dict = {
							'tuple_id': a.id,
							'year': a.year,
							'achievement_type': a.achievement_type,
							'title': a.title,
							'details': a.details,
							'organization': a.organization,
							'link': a.link					
						}			
						wl = profile_achievements_add_editForm(a_dict)
						achEditForm.append(wl)
					achInfoForm = zip(achEditForm, achDataCounter)
				achievementsaddForm = profile_achievements_add_editForm()

				#publicationForm populate and edit
				pubData = publication.objects.filter(user_id = User_obj)
				if len(pubData) == 0:
					pubData = 'unavailable'
					pubInfoForm = None
				else:
					copy_pubData = pubData
					pubDataCounter = range(len(copy_pubData))
					pubData = zip(copy_pubData, pubDataCounter)
					pubEditForm = []
					for p in copy_pubData:
						p_dict = {
							'tuple_id': p.id,
							'year': p.year,
							'mode': p.mode,
							'journal': p.journal,
							'status': p.status,				
							'details': p.details,					
							'link': p.link					
						}			
						wl = profile_publications_add_editForm(p_dict)
						pubEditForm.append(wl)
					pubInfoForm = zip(pubEditForm, pubDataCounter)
				publicationaddForm = profile_publications_add_editForm()

				#patentForm populate and edit
				patData = patent.objects.filter(user_id = User_obj)
				if len(patData) == 0:
					patData = 'unavailable'
					patInfoForm = None
				else:
					copy_patData = patData
					patDataCounter = range(len(copy_patData))
					patData = zip(copy_patData, patDataCounter)
					patEditForm = []
					for pa in copy_patData:
						pa_dict = {
							'tuple_id': pa.id,
							'year': pa.year,
							'mode': pa.mode,					
							'status': pa.patent_status,				
							'details': pa.patent_details
						}			
						wl = profile_patent_add_editForm(pa_dict)
						patEditForm.append(wl)
					patInfoForm = zip(patEditForm, patDataCounter)
				patentaddForm = profile_patent_add_editForm()

				skillsData = skills.objects.filter(user_id = User_obj)
				if len(skillsData) == 0:
					skillsData = 'unavailable'
					skillsInfoForm = None
				else:
					counter = 1
					skill_name_text = ''
					for s in skillsData:
						if counter == 1:
							skill_name_text = s.skill_name
						else:
							skill_name_text = skill_name_text + ',' + s.skill_name
						counter = counter + 1

					s_dict = {
						'skill': skill_name_text
					}
					skillsInfoForm = profile_skills_add_editForm(s_dict)
				skillsaddForm = profile_skills_add_editForm()

				variables = RequestContext(request, {
					'workForm': workForm,
					'educationForm': educationForm,
					'certificationForm': certificationForm,
					'publicationForm': publicationForm,
					'extracurricularForm': extracurricularForm,
					'patentForm': patentForm,
					'achievementForm': achievementForm,
					'aboutForm': aboutForm,
					'educationaddForm': educationaddForm,
					'workaddForm': workaddForm,
					'extracurricularaddForm': extracurricularaddForm,
					'certificationaddForm': certificationaddForm,
					'achievementsaddForm': achievementsaddForm,
					'publicationaddForm': publicationaddForm,
					'patentaddForm': patentaddForm,
					'aboutData': aboutData_existing,
					'educationData': educationData,	
					'educationInfoForm': educationInfoForm,
					'workData': workData,
					'workInfoForm': workInfoForm,
					'certificationData': certificationData,
					'certificationInfoForm': certificationInfoForm,
					'exData': exData,
					'exInfoForm': exInfoForm,
					'achData': achData,
					'achInfoForm': achInfoForm,
					'pubData': pubData,
					'pubInfoForm': pubInfoForm,
					'patData': patData,
					'patInfoForm': patInfoForm,
					'skillsaddForm': skillsaddForm,
					'skillsData': skillsData,
					'skillsInfoForm': skillsInfoForm,
					't_educationData': t_educationData,
					't_workData': t_workData,
					't_certificationData': t_certificationData,
					't_extracurricularData': t_extracurricularData,
					't_achievementData': t_achievementData,
					't_publicationData': t_publicationData,
					't_patentData': t_patentData
				})
				return render_to_response('profile-page.html', variables)

			else:
				client = workaddForm.cleaned_data['freelancer_client']
				title = workaddForm.cleaned_data['freelancer_project_title']
				status = workaddForm.cleaned_data['freelancer_project_status']
				link = workaddForm.cleaned_data['freelancer_link']
				year = workaddForm.cleaned_data['freelancer_year']

				work_obj = work(
					user_id = User_obj,
					work_type = 'Freelancer',
					freelancer_client_name = client,
					freelancer_project_title = title,
					freelancer_status = status,
					freelancer_link = link,
					freelancer_project_year = year
				)
				work_obj.save()
				status = {
					'error': False,
					'error_message': '',
					'success': True,
					'success_message': 'Work details saved.',
				}
				workForm = profile_workForm()
				educationForm = profile_educationForm()
				certificationForm = profile_certificationForm()
				publicationForm = profile_publicationForm()
				extracurricularForm = profile_extracurricularForm()
				patentForm = profile_patentForm()
				achievementForm = profile_achievementForm()
				t_educationData = education.objects.filter(user_id = User_obj)
				if len(t_educationData) == 0:
					t_educationData = 'unavailable'
				else:
					t_educationData = zip(t_educationData, range(len(t_educationData)))
				t_workData = work.objects.filter(user_id = User_obj)
				if len(t_workData) == 0:
					t_workData = 'unavailable'
				else:
					t_workData = zip(t_workData, range(len(t_workData)))
				t_certificationData = certification.objects.filter(user_id = User_obj)
				if len(t_certificationData) == 0:
					t_certificationData = 'unavailable'
				else:
					t_certificationData = zip(t_certificationData, range(len(t_certificationData)))
				t_extracurricularData = extracurricular_activities.objects.filter(user_id = User_obj)
				if len(t_extracurricularData) == 0:
					t_extracurricularData = 'unavailable'
				else:
					t_extracurricularData = zip(t_extracurricularData, range(len(t_extracurricularData)))
				t_achievementData = achievements.objects.filter(user_id = User_obj)
				if len(t_achievementData) == 0:
					t_achievementData = 'unavailable'
				else:
					t_achievementData = zip(t_achievementData, range(len(t_achievementData)))
				t_publicationData = publication.objects.filter(user_id = User_obj)
				if len(t_publicationData) == 0:
					t_publicationData = 'unavailable'
				else:
					t_publicationData = zip(t_publicationData, range(len(t_publicationData)))
				t_patentData = patent.objects.filter(user_id = User_obj)					
				if len(t_patentData) == 0:
					t_patentData = 'unavailable'
				else:
					t_patentData = zip(t_patentData, range(len(t_patentData)))


				
				# aboutForm population
				try:
					existing_about = user_details.objects.get(user_id = User_obj)
				except:
					existing_about = 'unavailable'
				if existing_about!='unavailable':
					aboutForm_existing = {
						'profession': existing_about.profession,
						'first_name': existing_about.first_name,
						'last_name': existing_about.last_name,
						'dob': existing_about.dob,
						'short_bio': existing_about.short_bio,
						'facebook_url': existing_about.facebook_url,
						'twitter_handle': existing_about.twitter_handle,
						'linkedin_url': existing_about.linkedin_url
					}
				else:
					aboutForm_existing = None
				aboutData_existing = aboutForm_existing
				aboutForm = profile_aboutmeForm(aboutForm_existing)

				#educationForm population and edit
				educationData = education.objects.filter(user_id = User_obj)
				if len(educationData) == 0:
					educationData = 'unavailable'
					educationInfoForm = None
				else:
					copy_educationData = educationData
					educationDataCounter = range(len(copy_educationData))
					educationData = zip(copy_educationData, educationDataCounter)
					educationEditForm = []
					for e in copy_educationData:
						e_dict = {
							'tuple_id': e.id,
							'year': e.year,
							'education_type': e.education_type,
							'institution': e.institution_name,
							'aggregate': e.aggregate,
							'what_did_you_do_there': e.what_did_you_do_there
						}
						el = profile_education_add_editForm(e_dict)
						educationEditForm.append(el)
					educationInfoForm = zip(educationEditForm, educationDataCounter)
				educationaddForm = profile_education_add_editForm()

				#workForm population and edit
				workData = work.objects.filter(user_id = User_obj)
				if len(workData) == 0:
					workData = 'unavailable'
					workInfoForm = None
				else:
					copy_workData = workData
					workDataCounter = range(len(copy_workData))
					workData = zip(copy_workData, workDataCounter)
					workEditForm = []
					for w in copy_workData:
						if w.work_type == 'Internship':
							w_dict = {
								'tuple_id': w.id,
								'work_type': w.work_type,
								'internship_company_name': w.internship_company_name,
								'internship_from_date': w.internship_date_from,
								'internship_to_date': w.internship_date_to,
								'internship_title': w.internship_title
							}
						elif w.work_type == 'Job':
							w_dict = {
								'tuple_id': w.id,
								'work_type': w.work_type,
								'job_company_name': w.job_company_name,
								'job_designation': w.job_designation,
								'job_from_date': w.job_date_from,
								'job_to_date': w.job_date_to
							}
						else:
							w_dict = {
								'tuple_id': w.id,
								'work_type': w.work_type,
								'freelancer_client': w.freelancer_client_name,
								'freelancer_project_title': w.freelancer_project_title,
								'freelancer_link': w.freelancer_link,
								'freelancer_project_status': w.freelancer_status,
								'freelancer_year': w.freelancer_year
							}
						wl = profile_work_add_editForm(w_dict)
						workEditForm.append(wl)
					workInfoForm = zip(workEditForm, workDataCounter)
				workaddForm = profile_work_add_editForm()

				#certificationForm populate and edit
				certificationData = certification.objects.filter(user_id = User_obj)
				if len(certificationData) == 0:
					certificationData = 'unavailable'
					certificationInfoForm = None
				else:
					copy_certificationData = certificationData
					certificationDataCounter = range(len(copy_certificationData))
					certificationData = zip(copy_certificationData, certificationDataCounter)
					certificationEditForm = []
					for c in copy_certificationData:
						c_dict = {
							'tuple_id': c.id,
							'year': c.year,
							'agency': c.agency,
							'mode': c.mode_of_certification,
							'details': c.details,					
						}		
						wl = profile_certification_add_editForm(c_dict)
						certificationEditForm.append(wl)
					certificationInfoForm = zip(certificationEditForm, certificationDataCounter)
				certificationaddForm = profile_certification_add_editForm()

				#extracurricularForm populate and edit
				exData = extracurricular_activities.objects.filter(user_id = User_obj)
				if len(exData) == 0:
					exData = 'unavailable'
					exInfoForm = None
				else:
					copy_exData = exData
					exDataCounter = range(len(copy_exData))
					exData = zip(copy_exData, exDataCounter)
					exEditForm = []
					for e in copy_exData:
						e_dict = {
							'tuple_id': e.id,
							'year': e.year,
							'activity_type': e.activity_type,
							'title': e.title,
							'details': e.activity_details,
							'organization': e.organization,
							'link': e.link					
						}			
						wl = profile_extracurricular_add_editForm(e_dict)
						exEditForm.append(wl)
					exInfoForm = zip(exEditForm, exDataCounter)
				extracurricularaddForm = profile_extracurricular_add_editForm()

				#achievementForm populate and edit
				achData = achievements.objects.filter(user_id = User_obj)
				if len(achData) == 0:
					achData = 'unavailable'
					achInfoForm = None
				else:
					copy_achData = achData
					achDataCounter = range(len(copy_achData))
					achData = zip(copy_achData, achDataCounter)
					achEditForm = []
					for a in copy_achData:
						a_dict = {
							'tuple_id': a.id,
							'year': a.year,
							'achievement_type': a.achievement_type,
							'title': a.title,
							'details': a.details,
							'organization': a.organization,
							'link': a.link					
						}			
						wl = profile_achievements_add_editForm(a_dict)
						achEditForm.append(wl)
					achInfoForm = zip(achEditForm, achDataCounter)
				achievementsaddForm = profile_achievements_add_editForm()

				#publicationForm populate and edit
				pubData = publication.objects.filter(user_id = User_obj)
				if len(pubData) == 0:
					pubData = 'unavailable'
					pubInfoForm = None
				else:
					copy_pubData = pubData
					pubDataCounter = range(len(copy_pubData))
					pubData = zip(copy_pubData, pubDataCounter)
					pubEditForm = []
					for p in copy_pubData:
						p_dict = {
							'tuple_id': p.id,
							'year': p.year,
							'mode': p.mode,
							'journal': p.journal,
							'status': p.status,				
							'details': p.details,					
							'link': p.link					
						}			
						wl = profile_publications_add_editForm(p_dict)
						pubEditForm.append(wl)
					pubInfoForm = zip(pubEditForm, pubDataCounter)
				publicationaddForm = profile_publications_add_editForm()

				#patentForm populate and edit
				patData = patent.objects.filter(user_id = User_obj)
				if len(patData) == 0:
					patData = 'unavailable'
					patInfoForm = None
				else:
					copy_patData = patData
					patDataCounter = range(len(copy_patData))
					patData = zip(copy_patData, patDataCounter)
					patEditForm = []
					for pa in copy_patData:
						pa_dict = {
							'tuple_id': pa.id,
							'year': pa.year,
							'mode': pa.mode,					
							'status': pa.patent_status,				
							'details': pa.patent_details
						}			
						wl = profile_patent_add_editForm(pa_dict)
						patEditForm.append(wl)
					patInfoForm = zip(patEditForm, patDataCounter)
				patentaddForm = profile_patent_add_editForm()

				skillsData = skills.objects.filter(user_id = User_obj)
				if len(skillsData) == 0:
					skillsData = 'unavailable'
					skillsInfoForm = None
				else:
					counter = 1
					skill_name_text = ''
					for s in skillsData:
						if counter == 1:
							skill_name_text = s.skill_name
						else:
							skill_name_text = skill_name_text + ',' + s.skill_name
						counter = counter + 1

					s_dict = {
						'skill': skill_name_text
					}
					skillsInfoForm = profile_skills_add_editForm(s_dict)
				skillsaddForm = profile_skills_add_editForm()

				variables = RequestContext(request, {
					'workForm': workForm,
					'educationForm': educationForm,
					'certificationForm': certificationForm,
					'publicationForm': publicationForm,
					'extracurricularForm': extracurricularForm,
					'patentForm': patentForm,
					'achievementForm': achievementForm,
					'aboutForm': aboutForm,
					'educationaddForm': educationaddForm,
					'workaddForm': workaddForm,
					'extracurricularaddForm': extracurricularaddForm,
					'certificationaddForm': certificationaddForm,
					'achievementsaddForm': achievementsaddForm,
					'publicationaddForm': publicationaddForm,
					'patentaddForm': patentaddForm,
					'aboutData': aboutData_existing,
					'educationData': educationData,	
					'educationInfoForm': educationInfoForm,
					'workData': workData,
					'workInfoForm': workInfoForm,
					'certificationData': certificationData,
					'certificationInfoForm': certificationInfoForm,
					'exData': exData,
					'exInfoForm': exInfoForm,
					'achData': achData,
					'achInfoForm': achInfoForm,
					'pubData': pubData,
					'pubInfoForm': pubInfoForm,
					'patData': patData,
					'patInfoForm': patInfoForm,
					'skillsaddForm': skillsaddForm,
					'skillsData': skillsData,
					'skillsInfoForm': skillsInfoForm,
					't_educationData': t_educationData,
					't_workData': t_workData,
					't_certificationData': t_certificationData,
					't_extracurricularData': t_extracurricularData,
					't_achievementData': t_achievementData,
					't_publicationData': t_publicationData,
					't_patentData': t_patentData
				})
				return render_to_response('profile-page.html', variables)

	elif request.method=='POST' and 'educationaddForm' in request.POST:
		educationaddForm = profile_education_add_editForm(request.POST, request.FILES)
		if educationaddForm.is_valid():
			year = educationaddForm.cleaned_data['year']
			education_type = educationaddForm.cleaned_data['education_type']
			institution = educationaddForm.cleaned_data['institution']
			aggregate = educationaddForm.cleaned_data['aggregate']
			what_did_you_do_there = educationaddForm.cleaned_data['what_did_you_do_there']
			attached_file = educationaddForm.cleaned_data['attach_file']

			education_obj = education(
				user_id = User_obj,
				year = year,
				education_type = education_type,
				institution_name = institution,
				aggregate = aggregate,
				what_did_you_do_there = what_did_you_do_there,
				document = attached_file
			)
			education_obj.save()
			status = {
				'error': False,
				'error_message': '',
				'success': True,
				'success_message': 'Education details saved.',
			}
			workForm = profile_workForm()
			educationForm = profile_educationForm()
			certificationForm = profile_certificationForm()
			publicationForm = profile_publicationForm()
			extracurricularForm = profile_extracurricularForm()
			patentForm = profile_patentForm()
			achievementForm = profile_achievementForm()
			t_educationData = education.objects.filter(user_id = User_obj)
			if len(t_educationData) == 0:
				t_educationData = 'unavailable'
			else:
				t_educationData = zip(t_educationData, range(len(t_educationData)))
			t_workData = work.objects.filter(user_id = User_obj)
			if len(t_workData) == 0:
				t_workData = 'unavailable'
			else:
				t_workData = zip(t_workData, range(len(t_workData)))
			t_certificationData = certification.objects.filter(user_id = User_obj)
			if len(t_certificationData) == 0:
				t_certificationData = 'unavailable'
			else:
				t_certificationData = zip(t_certificationData, range(len(t_certificationData)))
			t_extracurricularData = extracurricular_activities.objects.filter(user_id = User_obj)
			if len(t_extracurricularData) == 0:
				t_extracurricularData = 'unavailable'
			else:
				t_extracurricularData = zip(t_extracurricularData, range(len(t_extracurricularData)))
			t_achievementData = achievements.objects.filter(user_id = User_obj)
			if len(t_achievementData) == 0:
				t_achievementData = 'unavailable'
			else:
				t_achievementData = zip(t_achievementData, range(len(t_achievementData)))
			t_publicationData = publication.objects.filter(user_id = User_obj)
			if len(t_publicationData) == 0:
				t_publicationData = 'unavailable'
			else:
				t_publicationData = zip(t_publicationData, range(len(t_publicationData)))
			t_patentData = patent.objects.filter(user_id = User_obj)					
			if len(t_patentData) == 0:
				t_patentData = 'unavailable'
			else:
				t_patentData = zip(t_patentData, range(len(t_patentData)))


			
			# aboutForm population
			try:
				existing_about = user_details.objects.get(user_id = User_obj)
			except:
				existing_about = 'unavailable'
			if existing_about!='unavailable':
				aboutForm_existing = {
					'profession': existing_about.profession,
					'first_name': existing_about.first_name,
					'last_name': existing_about.last_name,
					'dob': existing_about.dob,
					'short_bio': existing_about.short_bio,
					'facebook_url': existing_about.facebook_url,
					'twitter_handle': existing_about.twitter_handle,
					'linkedin_url': existing_about.linkedin_url
				}

			else:
				aboutForm_existing = None
			aboutData_existing = aboutForm_existing
			aboutForm = profile_aboutmeForm(aboutForm_existing)

			#educationForm population and edit
			educationData = education.objects.filter(user_id = User_obj)
			if len(educationData) == 0:
				educationData = 'unavailable'
				educationInfoForm = None
			else:
				copy_educationData = educationData
				educationDataCounter = range(len(copy_educationData))
				educationData = zip(copy_educationData, educationDataCounter)
				educationEditForm = []
				for e in copy_educationData:
					e_dict = {
						'tuple_id': e.id,
						'year': e.year,
						'education_type': e.education_type,
						'institution': e.institution_name,
						'aggregate': e.aggregate,
						'what_did_you_do_there': e.what_did_you_do_there
					}
					el = profile_education_add_editForm(e_dict)
					educationEditForm.append(el)
				educationInfoForm = zip(educationEditForm, educationDataCounter)
			educationaddForm = profile_education_add_editForm()

			#workForm population and edit
			workData = work.objects.filter(user_id = User_obj)
			if len(workData) == 0:
				workData = 'unavailable'
				workInfoForm = None
			else:
				copy_workData = workData
				workDataCounter = range(len(copy_workData))
				workData = zip(copy_workData, workDataCounter)
				workEditForm = []
				for w in copy_workData:
					if w.work_type == 'Internship':
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'internship_company_name': w.internship_company_name,
							'internship_from_date': w.internship_date_from,
							'internship_to_date': w.internship_date_to,
							'internship_title': w.internship_title
						}
					elif w.work_type == 'Job':
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'job_company_name': w.job_company_name,
							'job_designation': w.job_designation,
							'job_from_date': w.job_date_from,
							'job_to_date': w.job_date_to
						}
					else:
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'freelancer_client': w.freelancer_client_name,
							'freelancer_project_title': w.freelancer_project_title,
							'freelancer_link': w.freelancer_link,
							'freelancer_project_status': w.freelancer_status,
							'freelancer_year': w.freelancer_year
						}
					wl = profile_work_add_editForm(w_dict)
					workEditForm.append(wl)
				workInfoForm = zip(workEditForm, workDataCounter)
			workaddForm = profile_work_add_editForm()

			#certificationForm populate and edit
			certificationData = certification.objects.filter(user_id = User_obj)
			if len(certificationData) == 0:
				certificationData = 'unavailable'
				certificationInfoForm = None
			else:
				copy_certificationData = certificationData
				certificationDataCounter = range(len(copy_certificationData))
				certificationData = zip(copy_certificationData, certificationDataCounter)
				certificationEditForm = []
				for c in copy_certificationData:
					c_dict = {
						'tuple_id': c.id,
						'year': c.year,
						'agency': c.agency,
						'mode': c.mode_of_certification,
						'details': c.details,					
					}		
					wl = profile_certification_add_editForm(c_dict)
					certificationEditForm.append(wl)
				certificationInfoForm = zip(certificationEditForm, certificationDataCounter)
			certificationaddForm = profile_certification_add_editForm()

			#extracurricularForm populate and edit
			exData = extracurricular_activities.objects.filter(user_id = User_obj)
			if len(exData) == 0:
				exData = 'unavailable'
				exInfoForm = None
			else:
				copy_exData = exData
				exDataCounter = range(len(copy_exData))
				exData = zip(copy_exData, exDataCounter)
				exEditForm = []
				for e in copy_exData:
					e_dict = {
						'tuple_id': e.id,
						'year': e.year,
						'activity_type': e.activity_type,
						'title': e.title,
						'details': e.activity_details,
						'organization': e.organization,
						'link': e.link					
					}			
					wl = profile_extracurricular_add_editForm(e_dict)
					exEditForm.append(wl)
				exInfoForm = zip(exEditForm, exDataCounter)
			extracurricularaddForm = profile_extracurricular_add_editForm()

			#achievementForm populate and edit
			achData = achievements.objects.filter(user_id = User_obj)
			if len(achData) == 0:
				achData = 'unavailable'
				achInfoForm = None
			else:
				copy_achData = achData
				achDataCounter = range(len(copy_achData))
				achData = zip(copy_achData, achDataCounter)
				achEditForm = []
				for a in copy_achData:
					a_dict = {
						'tuple_id': a.id,
						'year': a.year,
						'achievement_type': a.achievement_type,
						'title': a.title,
						'details': a.details,
						'organization': a.organization,
						'link': a.link					
					}			
					wl = profile_achievements_add_editForm(a_dict)
					achEditForm.append(wl)
				achInfoForm = zip(achEditForm, achDataCounter)
			achievementsaddForm = profile_achievements_add_editForm()

			#publicationForm populate and edit
			pubData = publication.objects.filter(user_id = User_obj)
			if len(pubData) == 0:
				pubData = 'unavailable'
				pubInfoForm = None
			else:
				copy_pubData = pubData
				pubDataCounter = range(len(copy_pubData))
				pubData = zip(copy_pubData, pubDataCounter)
				pubEditForm = []
				for p in copy_pubData:
					p_dict = {
						'tuple_id': p.id,
						'year': p.year,
						'mode': p.mode,
						'journal': p.journal,
						'status': p.status,				
						'details': p.details,					
						'link': p.link					
					}			
					wl = profile_publications_add_editForm(p_dict)
					pubEditForm.append(wl)
				pubInfoForm = zip(pubEditForm, pubDataCounter)
			publicationaddForm = profile_publications_add_editForm()

			#patentForm populate and edit
			patData = patent.objects.filter(user_id = User_obj)
			if len(patData) == 0:
				patData = 'unavailable'
				patInfoForm = None
			else:
				copy_patData = patData
				patDataCounter = range(len(copy_patData))
				patData = zip(copy_patData, patDataCounter)
				patEditForm = []
				for pa in copy_patData:
					pa_dict = {
						'tuple_id': pa.id,
						'year': pa.year,
						'mode': pa.mode,					
						'status': pa.patent_status,				
						'details': pa.patent_details
					}			
					wl = profile_patent_add_editForm(pa_dict)
					patEditForm.append(wl)
				patInfoForm = zip(patEditForm, patDataCounter)
			patentaddForm = profile_patent_add_editForm()

			skillsData = skills.objects.filter(user_id = User_obj)
			if len(skillsData) == 0:
				skillsData = 'unavailable'
				skillsInfoForm = None
			else:
				counter = 1
				skill_name_text = ''
				for s in skillsData:
					if counter == 1:
						skill_name_text = s.skill_name
					else:
						skill_name_text = skill_name_text + ',' + s.skill_name
					counter = counter + 1

				s_dict = {
					'skill': skill_name_text
				}
				skillsInfoForm = profile_skills_add_editForm(s_dict)
			skillsaddForm = profile_skills_add_editForm()

			variables = RequestContext(request, {
				'workForm': workForm,
				'educationForm': educationForm,
				'certificationForm': certificationForm,
				'publicationForm': publicationForm,
				'extracurricularForm': extracurricularForm,
				'patentForm': patentForm,
				'achievementForm': achievementForm,
				'aboutForm': aboutForm,
				'educationaddForm': educationaddForm,
				'workaddForm': workaddForm,
				'extracurricularaddForm': extracurricularaddForm,
				'certificationaddForm': certificationaddForm,
				'achievementsaddForm': achievementsaddForm,
				'publicationaddForm': publicationaddForm,
				'patentaddForm': patentaddForm,
				'aboutData': aboutData_existing,
				'educationData': educationData,	
				'educationInfoForm': educationInfoForm,
				'workData': workData,
				'workInfoForm': workInfoForm,
				'certificationData': certificationData,
				'certificationInfoForm': certificationInfoForm,
				'exData': exData,
				'exInfoForm': exInfoForm,
				'achData': achData,
				'achInfoForm': achInfoForm,
				'pubData': pubData,
				'pubInfoForm': pubInfoForm,
				'patData': patData,
				'patInfoForm': patInfoForm,
				'skillsaddForm': skillsaddForm,
				'skillsData': skillsData,
				'skillsInfoForm': skillsInfoForm,
				't_educationData': t_educationData,
				't_workData': t_workData,
				't_certificationData': t_certificationData,
				't_extracurricularData': t_extracurricularData,
				't_achievementData': t_achievementData,
				't_publicationData': t_publicationData,
				't_patentData': t_patentData
			})
			return render_to_response('profile-page.html', variables)

	elif request.method=='GET' and 'educationeditForm' in request.GET:
		educationaddForm = profile_education_add_editForm(request.GET)
		if educationaddForm.is_valid():
			row_id = educationaddForm.cleaned_data['tuple_id']
			year = educationaddForm.cleaned_data['year']
			education_type = educationaddForm.cleaned_data['education_type']
			institution = educationaddForm.cleaned_data['institution']
			aggregate = educationaddForm.cleaned_data['aggregate']
			what_did_you_do_there = educationaddForm.cleaned_data['what_did_you_do_there']
			# attached_file = request.FILES['attach_file']

			education_obj = education.objects.get(id = row_id)

			education_obj.year = year
			education_obj.education_type = education_type
			education_obj.institution_name = institution
			education_obj.aggregate = aggregate
			education_obj.what_did_you_do_there = what_did_you_do_there

			education_obj.save()

			status = {
				'error': False,
				'error_message': '',
				'success': True,
				'success_message': 'Education details saved.',
			}
			workForm = profile_workForm()
			educationForm = profile_educationForm()
			certificationForm = profile_certificationForm()
			publicationForm = profile_publicationForm()
			extracurricularForm = profile_extracurricularForm()
			patentForm = profile_patentForm()
			achievementForm = profile_achievementForm()
			t_educationData = education.objects.filter(user_id = User_obj)
			if len(t_educationData) == 0:
				t_educationData = 'unavailable'
			else:
				t_educationData = zip(t_educationData, range(len(t_educationData)))
			t_workData = work.objects.filter(user_id = User_obj)
			if len(t_workData) == 0:
				t_workData = 'unavailable'
			else:
				t_workData = zip(t_workData, range(len(t_workData)))
			t_certificationData = certification.objects.filter(user_id = User_obj)
			if len(t_certificationData) == 0:
				t_certificationData = 'unavailable'
			else:
				t_certificationData = zip(t_certificationData, range(len(t_certificationData)))
			t_extracurricularData = extracurricular_activities.objects.filter(user_id = User_obj)
			if len(t_extracurricularData) == 0:
				t_extracurricularData = 'unavailable'
			else:
				t_extracurricularData = zip(t_extracurricularData, range(len(t_extracurricularData)))
			t_achievementData = achievements.objects.filter(user_id = User_obj)
			if len(t_achievementData) == 0:
				t_achievementData = 'unavailable'
			else:
				t_achievementData = zip(t_achievementData, range(len(t_achievementData)))
			t_publicationData = publication.objects.filter(user_id = User_obj)
			if len(t_publicationData) == 0:
				t_publicationData = 'unavailable'
			else:
				t_publicationData = zip(t_publicationData, range(len(t_publicationData)))
			t_patentData = patent.objects.filter(user_id = User_obj)					
			if len(t_patentData) == 0:
				t_patentData = 'unavailable'
			else:
				t_patentData = zip(t_patentData, range(len(t_patentData)))


			
			# aboutForm population
			try:
				existing_about = user_details.objects.get(user_id = User_obj)
			except:
				existing_about = 'unavailable'
			if existing_about!='unavailable':
				aboutForm_existing = {
					'profession': existing_about.profession,
					'first_name': existing_about.first_name,
					'last_name': existing_about.last_name,
					'dob': existing_about.dob,
					'short_bio': existing_about.short_bio,
					'facebook_url': existing_about.facebook_url,
					'twitter_handle': existing_about.twitter_handle,
					'linkedin_url': existing_about.linkedin_url
				}
			else:
				aboutForm_existing = None
			aboutData_existing = aboutForm_existing
			aboutForm = profile_aboutmeForm(aboutForm_existing)

			#educationForm population and edit
			educationData = education.objects.filter(user_id = User_obj)
			if len(educationData) == 0:
				educationData = 'unavailable'
				educationInfoForm = None
			else:
				copy_educationData = educationData
				educationDataCounter = range(len(copy_educationData))
				educationData = zip(copy_educationData, educationDataCounter)
				educationEditForm = []
				for e in copy_educationData:
					e_dict = {
						'tuple_id': e.id,
						'year': e.year,
						'education_type': e.education_type,
						'institution': e.institution_name,
						'aggregate': e.aggregate,
						'what_did_you_do_there': e.what_did_you_do_there
					}
					el = profile_education_add_editForm(e_dict)
					educationEditForm.append(el)
				educationInfoForm = zip(educationEditForm, educationDataCounter)
			educationaddForm = profile_education_add_editForm()

			#workForm population and edit
			workData = work.objects.filter(user_id = User_obj)
			if len(workData) == 0:
				workData = 'unavailable'
				workInfoForm = None
			else:
				copy_workData = workData
				workDataCounter = range(len(copy_workData))
				workData = zip(copy_workData, workDataCounter)
				workEditForm = []
				for w in copy_workData:
					if w.work_type == 'Internship':
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'internship_company_name': w.internship_company_name,
							'internship_from_date': w.internship_date_from,
							'internship_to_date': w.internship_date_to,
							'internship_title': w.internship_title
						}
					elif w.work_type == 'Job':
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'job_company_name': w.job_company_name,
							'job_designation': w.job_designation,
							'job_from_date': w.job_date_from,
							'job_to_date': w.job_date_to
						}
					else:
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'freelancer_client': w.freelancer_client_name,
							'freelancer_project_title': w.freelancer_project_title,
							'freelancer_link': w.freelancer_link,
							'freelancer_project_status': w.freelancer_status,
							'freelancer_year': w.freelancer_year
						}
					wl = profile_work_add_editForm(w_dict)
					workEditForm.append(wl)
				workInfoForm = zip(workEditForm, workDataCounter)
			workaddForm = profile_work_add_editForm()

			#certificationForm populate and edit
			certificationData = certification.objects.filter(user_id = User_obj)
			if len(certificationData) == 0:
				certificationData = 'unavailable'
				certificationInfoForm = None
			else:
				copy_certificationData = certificationData
				certificationDataCounter = range(len(copy_certificationData))
				certificationData = zip(copy_certificationData, certificationDataCounter)
				certificationEditForm = []
				for c in copy_certificationData:
					c_dict = {
						'tuple_id': c.id,
						'year': c.year,
						'agency': c.agency,
						'mode': c.mode_of_certification,
						'details': c.details,					
					}		
					wl = profile_certification_add_editForm(c_dict)
					certificationEditForm.append(wl)
				certificationInfoForm = zip(certificationEditForm, certificationDataCounter)
			certificationaddForm = profile_certification_add_editForm()

			#extracurricularForm populate and edit
			exData = extracurricular_activities.objects.filter(user_id = User_obj)
			if len(exData) == 0:
				exData = 'unavailable'
				exInfoForm = None
			else:
				copy_exData = exData
				exDataCounter = range(len(copy_exData))
				exData = zip(copy_exData, exDataCounter)
				exEditForm = []
				for e in copy_exData:
					e_dict = {
						'tuple_id': e.id,
						'year': e.year,
						'activity_type': e.activity_type,
						'title': e.title,
						'details': e.activity_details,
						'organization': e.organization,
						'link': e.link					
					}			
					wl = profile_extracurricular_add_editForm(e_dict)
					exEditForm.append(wl)
				exInfoForm = zip(exEditForm, exDataCounter)
			extracurricularaddForm = profile_extracurricular_add_editForm()

			#achievementForm populate and edit
			achData = achievements.objects.filter(user_id = User_obj)
			if len(achData) == 0:
				achData = 'unavailable'
				achInfoForm = None
			else:
				copy_achData = achData
				achDataCounter = range(len(copy_achData))
				achData = zip(copy_achData, achDataCounter)
				achEditForm = []
				for a in copy_achData:
					a_dict = {
						'tuple_id': a.id,
						'year': a.year,
						'achievement_type': a.achievement_type,
						'title': a.title,
						'details': a.details,
						'organization': a.organization,
						'link': a.link					
					}			
					wl = profile_achievements_add_editForm(a_dict)
					achEditForm.append(wl)
				achInfoForm = zip(achEditForm, achDataCounter)
			achievementsaddForm = profile_achievements_add_editForm()

			#publicationForm populate and edit
			pubData = publication.objects.filter(user_id = User_obj)
			if len(pubData) == 0:
				pubData = 'unavailable'
				pubInfoForm = None
			else:
				copy_pubData = pubData
				pubDataCounter = range(len(copy_pubData))
				pubData = zip(copy_pubData, pubDataCounter)
				pubEditForm = []
				for p in copy_pubData:
					p_dict = {
						'tuple_id': p.id,
						'year': p.year,
						'mode': p.mode,
						'journal': p.journal,
						'status': p.status,				
						'details': p.details,					
						'link': p.link					
					}			
					wl = profile_publications_add_editForm(p_dict)
					pubEditForm.append(wl)
				pubInfoForm = zip(pubEditForm, pubDataCounter)
			publicationaddForm = profile_publications_add_editForm()

			#patentForm populate and edit
			patData = patent.objects.filter(user_id = User_obj)
			if len(patData) == 0:
				patData = 'unavailable'
				patInfoForm = None
			else:
				copy_patData = patData
				patDataCounter = range(len(copy_patData))
				patData = zip(copy_patData, patDataCounter)
				patEditForm = []
				for pa in copy_patData:
					pa_dict = {
						'tuple_id': pa.id,
						'year': pa.year,
						'mode': pa.mode,					
						'status': pa.patent_status,				
						'details': pa.patent_details
					}			
					wl = profile_patent_add_editForm(pa_dict)
					patEditForm.append(wl)
				patInfoForm = zip(patEditForm, patDataCounter)
			patentaddForm = profile_patent_add_editForm()

			skillsData = skills.objects.filter(user_id = User_obj)
			if len(skillsData) == 0:
				skillsData = 'unavailable'
				skillsInfoForm = None
			else:
				counter = 1
				skill_name_text = ''
				for s in skillsData:
					if counter == 1:
						skill_name_text = s.skill_name
					else:
						skill_name_text = skill_name_text + ',' + s.skill_name
					counter = counter + 1

				s_dict = {
					'skill': skill_name_text
				}
				skillsInfoForm = profile_skills_add_editForm(s_dict)
			skillsaddForm = profile_skills_add_editForm()

			variables = RequestContext(request, {
				'workForm': workForm,
				'educationForm': educationForm,
				'certificationForm': certificationForm,
				'publicationForm': publicationForm,
				'extracurricularForm': extracurricularForm,
				'patentForm': patentForm,
				'achievementForm': achievementForm,
				'aboutForm': aboutForm,
				'educationaddForm': educationaddForm,
				'workaddForm': workaddForm,
				'extracurricularaddForm': extracurricularaddForm,
				'certificationaddForm': certificationaddForm,
				'achievementsaddForm': achievementsaddForm,
				'publicationaddForm': publicationaddForm,
				'patentaddForm': patentaddForm,
				'aboutData': aboutData_existing,
				'educationData': educationData,	
				'educationInfoForm': educationInfoForm,
				'workData': workData,
				'workInfoForm': workInfoForm,
				'certificationData': certificationData,
				'certificationInfoForm': certificationInfoForm,
				'exData': exData,
				'exInfoForm': exInfoForm,
				'achData': achData,
				'achInfoForm': achInfoForm,
				'pubData': pubData,
				'pubInfoForm': pubInfoForm,
				'patData': patData,
				'patInfoForm': patInfoForm,
				'skillsaddForm': skillsaddForm,
				'skillsData': skillsData,
				'skillsInfoForm': skillsInfoForm,
				't_educationData': t_educationData,
				't_workData': t_workData,
				't_certificationData': t_certificationData,
				't_extracurricularData': t_extracurricularData,
				't_achievementData': t_achievementData,
				't_publicationData': t_publicationData,
				't_patentData': t_patentData
			})
			return render_to_response('profile-page.html', variables)

	elif request.method=='GET' and 'educationdeleteForm' in request.GET:
		educationaddForm = profile_education_add_editForm(request.GET)
		if educationaddForm.is_valid():
			row_id = educationaddForm.cleaned_data['tuple_id']
			# year = educationaddForm.cleaned_data['year']
			# education_type = educationaddForm.cleaned_data['education_type']
			# institution = educationaddForm.cleaned_data['institution']
			# aggregate = educationaddForm.cleaned_data['aggregate']
			# what_did_you_do_there = educationaddForm.cleaned_data['what_did_you_do_there']
			# attached_file = request.FILES['attach_file']

			education_obj = education.objects.get(id = row_id)

			education_obj.delete()

			status = {
				'error': False,
				'error_message': '',
				'success': True,
				'success_message': 'Education details deleted.',
			}
			workForm = profile_workForm()
			educationForm = profile_educationForm()
			certificationForm = profile_certificationForm()
			publicationForm = profile_publicationForm()
			extracurricularForm = profile_extracurricularForm()
			patentForm = profile_patentForm()
			achievementForm = profile_achievementForm()
			t_educationData = education.objects.filter(user_id = User_obj)
			if len(t_educationData) == 0:
				t_educationData = 'unavailable'
			else:
				t_educationData = zip(t_educationData, range(len(t_educationData)))
			t_workData = work.objects.filter(user_id = User_obj)
			if len(t_workData) == 0:
				t_workData = 'unavailable'
			else:
				t_workData = zip(t_workData, range(len(t_workData)))
			t_certificationData = certification.objects.filter(user_id = User_obj)
			if len(t_certificationData) == 0:
				t_certificationData = 'unavailable'
			else:
				t_certificationData = zip(t_certificationData, range(len(t_certificationData)))
			t_extracurricularData = extracurricular_activities.objects.filter(user_id = User_obj)
			if len(t_extracurricularData) == 0:
				t_extracurricularData = 'unavailable'
			else:
				t_extracurricularData = zip(t_extracurricularData, range(len(t_extracurricularData)))
			t_achievementData = achievements.objects.filter(user_id = User_obj)
			if len(t_achievementData) == 0:
				t_achievementData = 'unavailable'
			else:
				t_achievementData = zip(t_achievementData, range(len(t_achievementData)))
			t_publicationData = publication.objects.filter(user_id = User_obj)
			if len(t_publicationData) == 0:
				t_publicationData = 'unavailable'
			else:
				t_publicationData = zip(t_publicationData, range(len(t_publicationData)))
			t_patentData = patent.objects.filter(user_id = User_obj)					
			if len(t_patentData) == 0:
				t_patentData = 'unavailable'
			else:
				t_patentData = zip(t_patentData, range(len(t_patentData)))


			
			# aboutForm population
			try:
				existing_about = user_details.objects.get(user_id = User_obj)
			except:
				existing_about = 'unavailable'
			if existing_about!='unavailable':
				aboutForm_existing = {
					'profession': existing_about.profession,
					'first_name': existing_about.first_name,
					'last_name': existing_about.last_name,
					'dob': existing_about.dob,
					'short_bio': existing_about.short_bio,
					'facebook_url': existing_about.facebook_url,
					'twitter_handle': existing_about.twitter_handle,
					'linkedin_url': existing_about.linkedin_url
				}
			else:
				aboutForm_existing = None
			aboutData_existing = aboutForm_existing
			aboutForm = profile_aboutmeForm(aboutForm_existing)

			#educationForm population and edit
			educationData = education.objects.filter(user_id = User_obj)
			if len(educationData) == 0:
				educationData = 'unavailable'
				educationInfoForm = None
			else:
				copy_educationData = educationData
				educationDataCounter = range(len(copy_educationData))
				educationData = zip(copy_educationData, educationDataCounter)
				educationEditForm = []
				for e in copy_educationData:
					e_dict = {
						'tuple_id': e.id,
						'year': e.year,
						'education_type': e.education_type,
						'institution': e.institution_name,
						'aggregate': e.aggregate,
						'what_did_you_do_there': e.what_did_you_do_there
					}
					el = profile_education_add_editForm(e_dict)
					educationEditForm.append(el)
				educationInfoForm = zip(educationEditForm, educationDataCounter)
			educationaddForm = profile_education_add_editForm()

			#workForm population and edit
			workData = work.objects.filter(user_id = User_obj)
			if len(workData) == 0:
				workData = 'unavailable'
				workInfoForm = None
			else:
				copy_workData = workData
				workDataCounter = range(len(copy_workData))
				workData = zip(copy_workData, workDataCounter)
				workEditForm = []
				for w in copy_workData:
					if w.work_type == 'Internship':
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'internship_company_name': w.internship_company_name,
							'internship_from_date': w.internship_date_from,
							'internship_to_date': w.internship_date_to,
							'internship_title': w.internship_title
						}
					elif w.work_type == 'Job':
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'job_company_name': w.job_company_name,
							'job_designation': w.job_designation,
							'job_from_date': w.job_date_from,
							'job_to_date': w.job_date_to
						}
					else:
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'freelancer_client': w.freelancer_client_name,
							'freelancer_project_title': w.freelancer_project_title,
							'freelancer_link': w.freelancer_link,
							'freelancer_project_status': w.freelancer_status,
							'freelancer_year': w.freelancer_year
						}
					wl = profile_work_add_editForm(w_dict)
					workEditForm.append(wl)
				workInfoForm = zip(workEditForm, workDataCounter)
			workaddForm = profile_work_add_editForm()

			#certificationForm populate and edit
			certificationData = certification.objects.filter(user_id = User_obj)
			if len(certificationData) == 0:
				certificationData = 'unavailable'
				certificationInfoForm = None
			else:
				copy_certificationData = certificationData
				certificationDataCounter = range(len(copy_certificationData))
				certificationData = zip(copy_certificationData, certificationDataCounter)
				certificationEditForm = []
				for c in copy_certificationData:
					c_dict = {
						'tuple_id': c.id,
						'year': c.year,
						'agency': c.agency,
						'mode': c.mode_of_certification,
						'details': c.details,					
					}		
					wl = profile_certification_add_editForm(c_dict)
					certificationEditForm.append(wl)
				certificationInfoForm = zip(certificationEditForm, certificationDataCounter)
			certificationaddForm = profile_certification_add_editForm()

			#extracurricularForm populate and edit
			exData = extracurricular_activities.objects.filter(user_id = User_obj)
			if len(exData) == 0:
				exData = 'unavailable'
				exInfoForm = None
			else:
				copy_exData = exData
				exDataCounter = range(len(copy_exData))
				exData = zip(copy_exData, exDataCounter)
				exEditForm = []
				for e in copy_exData:
					e_dict = {
						'tuple_id': e.id,
						'year': e.year,
						'activity_type': e.activity_type,
						'title': e.title,
						'details': e.activity_details,
						'organization': e.organization,
						'link': e.link					
					}			
					wl = profile_extracurricular_add_editForm(e_dict)
					exEditForm.append(wl)
				exInfoForm = zip(exEditForm, exDataCounter)
			extracurricularaddForm = profile_extracurricular_add_editForm()

			#achievementForm populate and edit
			achData = achievements.objects.filter(user_id = User_obj)
			if len(achData) == 0:
				achData = 'unavailable'
				achInfoForm = None
			else:
				copy_achData = achData
				achDataCounter = range(len(copy_achData))
				achData = zip(copy_achData, achDataCounter)
				achEditForm = []
				for a in copy_achData:
					a_dict = {
						'tuple_id': a.id,
						'year': a.year,
						'achievement_type': a.achievement_type,
						'title': a.title,
						'details': a.details,
						'organization': a.organization,
						'link': a.link					
					}			
					wl = profile_achievements_add_editForm(a_dict)
					achEditForm.append(wl)
				achInfoForm = zip(achEditForm, achDataCounter)
			achievementsaddForm = profile_achievements_add_editForm()

			#publicationForm populate and edit
			pubData = publication.objects.filter(user_id = User_obj)
			if len(pubData) == 0:
				pubData = 'unavailable'
				pubInfoForm = None
			else:
				copy_pubData = pubData
				pubDataCounter = range(len(copy_pubData))
				pubData = zip(copy_pubData, pubDataCounter)
				pubEditForm = []
				for p in copy_pubData:
					p_dict = {
						'tuple_id': p.id,
						'year': p.year,
						'mode': p.mode,
						'journal': p.journal,
						'status': p.status,				
						'details': p.details,					
						'link': p.link					
					}			
					wl = profile_publications_add_editForm(p_dict)
					pubEditForm.append(wl)
				pubInfoForm = zip(pubEditForm, pubDataCounter)
			publicationaddForm = profile_publications_add_editForm()

			#patentForm populate and edit
			patData = patent.objects.filter(user_id = User_obj)
			if len(patData) == 0:
				patData = 'unavailable'
				patInfoForm = None
			else:
				copy_patData = patData
				patDataCounter = range(len(copy_patData))
				patData = zip(copy_patData, patDataCounter)
				patEditForm = []
				for pa in copy_patData:
					pa_dict = {
						'tuple_id': pa.id,
						'year': pa.year,
						'mode': pa.mode,					
						'status': pa.patent_status,				
						'details': pa.patent_details
					}			
					wl = profile_patent_add_editForm(pa_dict)
					patEditForm.append(wl)
				patInfoForm = zip(patEditForm, patDataCounter)
			patentaddForm = profile_patent_add_editForm()

			skillsData = skills.objects.filter(user_id = User_obj)
			if len(skillsData) == 0:
				skillsData = 'unavailable'
				skillsInfoForm = None
			else:
				counter = 1
				skill_name_text = ''
				for s in skillsData:
					if counter == 1:
						skill_name_text = s.skill_name
					else:
						skill_name_text = skill_name_text + ',' + s.skill_name
					counter = counter + 1

				s_dict = {
					'skill': skill_name_text
				}
				skillsInfoForm = profile_skills_add_editForm(s_dict)
			skillsaddForm = profile_skills_add_editForm()

			variables = RequestContext(request, {
				'workForm': workForm,
				'educationForm': educationForm,
				'certificationForm': certificationForm,
				'publicationForm': publicationForm,
				'extracurricularForm': extracurricularForm,
				'patentForm': patentForm,
				'achievementForm': achievementForm,
				'aboutForm': aboutForm,
				'educationaddForm': educationaddForm,
				'workaddForm': workaddForm,
				'extracurricularaddForm': extracurricularaddForm,
				'certificationaddForm': certificationaddForm,
				'achievementsaddForm': achievementsaddForm,
				'publicationaddForm': publicationaddForm,
				'patentaddForm': patentaddForm,
				'aboutData': aboutData_existing,
				'educationData': educationData,	
				'educationInfoForm': educationInfoForm,
				'workData': workData,
				'workInfoForm': workInfoForm,
				'certificationData': certificationData,
				'certificationInfoForm': certificationInfoForm,
				'exData': exData,
				'exInfoForm': exInfoForm,
				'achData': achData,
				'achInfoForm': achInfoForm,
				'pubData': pubData,
				'pubInfoForm': pubInfoForm,
				'patData': patData,
				'patInfoForm': patInfoForm,
				'skillsaddForm': skillsaddForm,
				'skillsData': skillsData,
				'skillsInfoForm': skillsInfoForm,
				't_educationData': t_educationData,
				't_workData': t_workData,
				't_certificationData': t_certificationData,
				't_extracurricularData': t_extracurricularData,
				't_achievementData': t_achievementData,
				't_publicationData': t_publicationData,
				't_patentData': t_patentData
			})
			return render_to_response('profile-page.html', variables)

	elif request.method=='GET' and 'certificationaddForm' in request.GET:
		certificationaddForm = profile_certification_add_editForm(request.GET)
		if certificationaddForm.is_valid():
			year = certificationaddForm.cleaned_data['year']
			agency = certificationaddForm.cleaned_data['agency']
			mode = certificationaddForm.cleaned_data['mode']
			details = certificationaddForm.cleaned_data['details']
			# attached_file = request.FILES['attach_file']

			certification_obj = certification(
				user_id = User_obj,
				year = year,
				agency = agency,
				mode_of_certification = mode,
				details = details,
				# document = attached_file
			)
			certification_obj.save()
			status = {
				'error': False,
				'error_message': '',
				'success': True,
				'success_message': 'Certification details saved.',
			}
			workForm = profile_workForm()
			educationForm = profile_educationForm()
			certificationForm = profile_certificationForm()
			publicationForm = profile_publicationForm()
			extracurricularForm = profile_extracurricularForm()
			patentForm = profile_patentForm()
			achievementForm = profile_achievementForm()
			t_educationData = education.objects.filter(user_id = User_obj)
			if len(t_educationData) == 0:
				t_educationData = 'unavailable'
			else:
				t_educationData = zip(t_educationData, range(len(t_educationData)))
			t_workData = work.objects.filter(user_id = User_obj)
			if len(t_workData) == 0:
				t_workData = 'unavailable'
			else:
				t_workData = zip(t_workData, range(len(t_workData)))
			t_certificationData = certification.objects.filter(user_id = User_obj)
			if len(t_certificationData) == 0:
				t_certificationData = 'unavailable'
			else:
				t_certificationData = zip(t_certificationData, range(len(t_certificationData)))
			t_extracurricularData = extracurricular_activities.objects.filter(user_id = User_obj)
			if len(t_extracurricularData) == 0:
				t_extracurricularData = 'unavailable'
			else:
				t_extracurricularData = zip(t_extracurricularData, range(len(t_extracurricularData)))
			t_achievementData = achievements.objects.filter(user_id = User_obj)
			if len(t_achievementData) == 0:
				t_achievementData = 'unavailable'
			else:
				t_achievementData = zip(t_achievementData, range(len(t_achievementData)))
			t_publicationData = publication.objects.filter(user_id = User_obj)
			if len(t_publicationData) == 0:
				t_publicationData = 'unavailable'
			else:
				t_publicationData = zip(t_publicationData, range(len(t_publicationData)))
			t_patentData = patent.objects.filter(user_id = User_obj)					
			if len(t_patentData) == 0:
				t_patentData = 'unavailable'
			else:
				t_patentData = zip(t_patentData, range(len(t_patentData)))


			
			# aboutForm population
			try:
				existing_about = user_details.objects.get(user_id = User_obj)
			except:
				existing_about = 'unavailable'
			if existing_about!='unavailable':
				aboutForm_existing = {
					'profession': existing_about.profession,
					'first_name': existing_about.first_name,
					'last_name': existing_about.last_name,
					'dob': existing_about.dob,
					'short_bio': existing_about.short_bio,
					'facebook_url': existing_about.facebook_url,
					'twitter_handle': existing_about.twitter_handle,
					'linkedin_url': existing_about.linkedin_url
				}
			else:
				aboutForm_existing = None
			aboutData_existing = aboutForm_existing
			aboutForm = profile_aboutmeForm(aboutForm_existing)

			#educationForm population and edit
			educationData = education.objects.filter(user_id = User_obj)
			if len(educationData) == 0:
				educationData = 'unavailable'
				educationInfoForm = None
			else:
				copy_educationData = educationData
				educationDataCounter = range(len(copy_educationData))
				educationData = zip(copy_educationData, educationDataCounter)
				educationEditForm = []
				for e in copy_educationData:
					e_dict = {
						'tuple_id': e.id,
						'year': e.year,
						'education_type': e.education_type,
						'institution': e.institution_name,
						'aggregate': e.aggregate,
						'what_did_you_do_there': e.what_did_you_do_there
					}
					el = profile_education_add_editForm(e_dict)
					educationEditForm.append(el)
				educationInfoForm = zip(educationEditForm, educationDataCounter)
			educationaddForm = profile_education_add_editForm()

			#workForm population and edit
			workData = work.objects.filter(user_id = User_obj)
			if len(workData) == 0:
				workData = 'unavailable'
				workInfoForm = None
			else:
				copy_workData = workData
				workDataCounter = range(len(copy_workData))
				workData = zip(copy_workData, workDataCounter)
				workEditForm = []
				for w in copy_workData:
					if w.work_type == 'Internship':
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'internship_company_name': w.internship_company_name,
							'internship_from_date': w.internship_date_from,
							'internship_to_date': w.internship_date_to,
							'internship_title': w.internship_title
						}
					elif w.work_type == 'Job':
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'job_company_name': w.job_company_name,
							'job_designation': w.job_designation,
							'job_from_date': w.job_date_from,
							'job_to_date': w.job_date_to
						}
					else:
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'freelancer_client': w.freelancer_client_name,
							'freelancer_project_title': w.freelancer_project_title,
							'freelancer_link': w.freelancer_link,
							'freelancer_project_status': w.freelancer_status,
							'freelancer_year': w.freelancer_year
						}
					wl = profile_work_add_editForm(w_dict)
					workEditForm.append(wl)
				workInfoForm = zip(workEditForm, workDataCounter)
			workaddForm = profile_work_add_editForm()

			#certificationForm populate and edit
			certificationData = certification.objects.filter(user_id = User_obj)
			if len(certificationData) == 0:
				certificationData = 'unavailable'
				certificationInfoForm = None
			else:
				copy_certificationData = certificationData
				certificationDataCounter = range(len(copy_certificationData))
				certificationData = zip(copy_certificationData, certificationDataCounter)
				certificationEditForm = []
				for c in copy_certificationData:
					c_dict = {
						'tuple_id': c.id,
						'year': c.year,
						'agency': c.agency,
						'mode': c.mode_of_certification,
						'details': c.details,					
					}		
					wl = profile_certification_add_editForm(c_dict)
					certificationEditForm.append(wl)
				certificationInfoForm = zip(certificationEditForm, certificationDataCounter)
			certificationaddForm = profile_certification_add_editForm()

			#extracurricularForm populate and edit
			exData = extracurricular_activities.objects.filter(user_id = User_obj)
			if len(exData) == 0:
				exData = 'unavailable'
				exInfoForm = None
			else:
				copy_exData = exData
				exDataCounter = range(len(copy_exData))
				exData = zip(copy_exData, exDataCounter)
				exEditForm = []
				for e in copy_exData:
					e_dict = {
						'tuple_id': e.id,
						'year': e.year,
						'activity_type': e.activity_type,
						'title': e.title,
						'details': e.activity_details,
						'organization': e.organization,
						'link': e.link					
					}			
					wl = profile_extracurricular_add_editForm(e_dict)
					exEditForm.append(wl)
				exInfoForm = zip(exEditForm, exDataCounter)
			extracurricularaddForm = profile_extracurricular_add_editForm()

			#achievementForm populate and edit
			achData = achievements.objects.filter(user_id = User_obj)
			if len(achData) == 0:
				achData = 'unavailable'
				achInfoForm = None
			else:
				copy_achData = achData
				achDataCounter = range(len(copy_achData))
				achData = zip(copy_achData, achDataCounter)
				achEditForm = []
				for a in copy_achData:
					a_dict = {
						'tuple_id': a.id,
						'year': a.year,
						'achievement_type': a.achievement_type,
						'title': a.title,
						'details': a.details,
						'organization': a.organization,
						'link': a.link					
					}			
					wl = profile_achievements_add_editForm(a_dict)
					achEditForm.append(wl)
				achInfoForm = zip(achEditForm, achDataCounter)
			achievementsaddForm = profile_achievements_add_editForm()

			#publicationForm populate and edit
			pubData = publication.objects.filter(user_id = User_obj)
			if len(pubData) == 0:
				pubData = 'unavailable'
				pubInfoForm = None
			else:
				copy_pubData = pubData
				pubDataCounter = range(len(copy_pubData))
				pubData = zip(copy_pubData, pubDataCounter)
				pubEditForm = []
				for p in copy_pubData:
					p_dict = {
						'tuple_id': p.id,
						'year': p.year,
						'mode': p.mode,
						'journal': p.journal,
						'status': p.status,				
						'details': p.details,					
						'link': p.link					
					}			
					wl = profile_publications_add_editForm(p_dict)
					pubEditForm.append(wl)
				pubInfoForm = zip(pubEditForm, pubDataCounter)
			publicationaddForm = profile_publications_add_editForm()

			#patentForm populate and edit
			patData = patent.objects.filter(user_id = User_obj)
			if len(patData) == 0:
				patData = 'unavailable'
				patInfoForm = None
			else:
				copy_patData = patData
				patDataCounter = range(len(copy_patData))
				patData = zip(copy_patData, patDataCounter)
				patEditForm = []
				for pa in copy_patData:
					pa_dict = {
						'tuple_id': pa.id,
						'year': pa.year,
						'mode': pa.mode,					
						'status': pa.patent_status,				
						'details': pa.patent_details
					}			
					wl = profile_patent_add_editForm(pa_dict)
					patEditForm.append(wl)
				patInfoForm = zip(patEditForm, patDataCounter)
			patentaddForm = profile_patent_add_editForm()

			skillsData = skills.objects.filter(user_id = User_obj)
			if len(skillsData) == 0:
				skillsData = 'unavailable'
				skillsInfoForm = None
			else:
				counter = 1
				skill_name_text = ''
				for s in skillsData:
					if counter == 1:
						skill_name_text = s.skill_name
					else:
						skill_name_text = skill_name_text + ',' + s.skill_name
					counter = counter + 1

				s_dict = {
					'skill': skill_name_text
				}
				skillsInfoForm = profile_skills_add_editForm(s_dict)
			skillsaddForm = profile_skills_add_editForm()

			variables = RequestContext(request, {
				'workForm': workForm,
				'educationForm': educationForm,
				'certificationForm': certificationForm,
				'publicationForm': publicationForm,
				'extracurricularForm': extracurricularForm,
				'patentForm': patentForm,
				'achievementForm': achievementForm,
				'aboutForm': aboutForm,
				'educationaddForm': educationaddForm,
				'workaddForm': workaddForm,
				'extracurricularaddForm': extracurricularaddForm,
				'certificationaddForm': certificationaddForm,
				'achievementsaddForm': achievementsaddForm,
				'publicationaddForm': publicationaddForm,
				'patentaddForm': patentaddForm,
				'aboutData': aboutData_existing,
				'educationData': educationData,	
				'educationInfoForm': educationInfoForm,
				'workData': workData,
				'workInfoForm': workInfoForm,
				'certificationData': certificationData,
				'certificationInfoForm': certificationInfoForm,
				'exData': exData,
				'exInfoForm': exInfoForm,
				'achData': achData,
				'achInfoForm': achInfoForm,
				'pubData': pubData,
				'pubInfoForm': pubInfoForm,
				'patData': patData,
				'patInfoForm': patInfoForm,
				'skillsaddForm': skillsaddForm,
				'skillsData': skillsData,
				'skillsInfoForm': skillsInfoForm,
				't_educationData': t_educationData,
				't_workData': t_workData,
				't_certificationData': t_certificationData,
				't_extracurricularData': t_extracurricularData,
				't_achievementData': t_achievementData,
				't_publicationData': t_publicationData,
				't_patentData': t_patentData
			})
			return render_to_response('profile-page.html', variables)

	elif request.method=='GET' and 'certificationeditForm' in request.GET:
		certificationaddForm = profile_certification_add_editForm(request.GET)
		if certificationaddForm.is_valid():
			row_id = certificationaddForm.cleaned_data['tuple_id']
			year = certificationaddForm.cleaned_data['year']
			agency = certificationaddForm.cleaned_data['agency']
			mode = certificationaddForm.cleaned_data['mode']
			details = certificationaddForm.cleaned_data['details']
			# attached_file = request.FILES['attach_file']

			certification_obj = certification.objects.get(id = row_id)

			certification_obj.year = year
			certification_obj.agency = agency
			certification_obj.mode_of_certification = mode
			certification_obj.details = details

			certification_obj.save()

			status = {
				'error': False,
				'error_message': '',
				'success': True,
				'success_message': 'Certification details saved.',
			}
			workForm = profile_workForm()
			educationForm = profile_educationForm()
			certificationForm = profile_certificationForm()
			publicationForm = profile_publicationForm()
			extracurricularForm = profile_extracurricularForm()
			patentForm = profile_patentForm()
			achievementForm = profile_achievementForm()
			t_educationData = education.objects.filter(user_id = User_obj)
			if len(t_educationData) == 0:
				t_educationData = 'unavailable'
			else:
				t_educationData = zip(t_educationData, range(len(t_educationData)))
			t_workData = work.objects.filter(user_id = User_obj)
			if len(t_workData) == 0:
				t_workData = 'unavailable'
			else:
				t_workData = zip(t_workData, range(len(t_workData)))
			t_certificationData = certification.objects.filter(user_id = User_obj)
			if len(t_certificationData) == 0:
				t_certificationData = 'unavailable'
			else:
				t_certificationData = zip(t_certificationData, range(len(t_certificationData)))
			t_extracurricularData = extracurricular_activities.objects.filter(user_id = User_obj)
			if len(t_extracurricularData) == 0:
				t_extracurricularData = 'unavailable'
			else:
				t_extracurricularData = zip(t_extracurricularData, range(len(t_extracurricularData)))
			t_achievementData = achievements.objects.filter(user_id = User_obj)
			if len(t_achievementData) == 0:
				t_achievementData = 'unavailable'
			else:
				t_achievementData = zip(t_achievementData, range(len(t_achievementData)))
			t_publicationData = publication.objects.filter(user_id = User_obj)
			if len(t_publicationData) == 0:
				t_publicationData = 'unavailable'
			else:
				t_publicationData = zip(t_publicationData, range(len(t_publicationData)))
			t_patentData = patent.objects.filter(user_id = User_obj)					
			if len(t_patentData) == 0:
				t_patentData = 'unavailable'
			else:
				t_patentData = zip(t_patentData, range(len(t_patentData)))


			
			# aboutForm population
			try:
				existing_about = user_details.objects.get(user_id = User_obj)
			except:
				existing_about = 'unavailable'
			if existing_about!='unavailable':
				aboutForm_existing = {
					'profession': existing_about.profession,
					'first_name': existing_about.first_name,
					'last_name': existing_about.last_name,
					'dob': existing_about.dob,
					'short_bio': existing_about.short_bio,
					'facebook_url': existing_about.facebook_url,
					'twitter_handle': existing_about.twitter_handle,
					'linkedin_url': existing_about.linkedin_url
				}
			else:
				aboutForm_existing = None
			aboutData_existing = aboutForm_existing
			aboutForm = profile_aboutmeForm(aboutForm_existing)

			#educationForm population and edit
			educationData = education.objects.filter(user_id = User_obj)
			if len(educationData) == 0:
				educationData = 'unavailable'
				educationInfoForm = None
			else:
				copy_educationData = educationData
				educationDataCounter = range(len(copy_educationData))
				educationData = zip(copy_educationData, educationDataCounter)
				educationEditForm = []
				for e in copy_educationData:
					e_dict = {
						'tuple_id': e.id,
						'year': e.year,
						'education_type': e.education_type,
						'institution': e.institution_name,
						'aggregate': e.aggregate,
						'what_did_you_do_there': e.what_did_you_do_there
					}
					el = profile_education_add_editForm(e_dict)
					educationEditForm.append(el)
				educationInfoForm = zip(educationEditForm, educationDataCounter)
			educationaddForm = profile_education_add_editForm()

			#workForm population and edit
			workData = work.objects.filter(user_id = User_obj)
			if len(workData) == 0:
				workData = 'unavailable'
				workInfoForm = None
			else:
				copy_workData = workData
				workDataCounter = range(len(copy_workData))
				workData = zip(copy_workData, workDataCounter)
				workEditForm = []
				for w in copy_workData:
					if w.work_type == 'Internship':
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'internship_company_name': w.internship_company_name,
							'internship_from_date': w.internship_date_from,
							'internship_to_date': w.internship_date_to,
							'internship_title': w.internship_title
						}
					elif w.work_type == 'Job':
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'job_company_name': w.job_company_name,
							'job_designation': w.job_designation,
							'job_from_date': w.job_date_from,
							'job_to_date': w.job_date_to
						}
					else:
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'freelancer_client': w.freelancer_client_name,
							'freelancer_project_title': w.freelancer_project_title,
							'freelancer_link': w.freelancer_link,
							'freelancer_project_status': w.freelancer_status,
							'freelancer_year': w.freelancer_year
						}
					wl = profile_work_add_editForm(w_dict)
					workEditForm.append(wl)
				workInfoForm = zip(workEditForm, workDataCounter)
			workaddForm = profile_work_add_editForm()

			#certificationForm populate and edit
			certificationData = certification.objects.filter(user_id = User_obj)
			if len(certificationData) == 0:
				certificationData = 'unavailable'
				certificationInfoForm = None
			else:
				copy_certificationData = certificationData
				certificationDataCounter = range(len(copy_certificationData))
				certificationData = zip(copy_certificationData, certificationDataCounter)
				certificationEditForm = []
				for c in copy_certificationData:
					c_dict = {
						'tuple_id': c.id,
						'year': c.year,
						'agency': c.agency,
						'mode': c.mode_of_certification,
						'details': c.details,					
					}		
					wl = profile_certification_add_editForm(c_dict)
					certificationEditForm.append(wl)
				certificationInfoForm = zip(certificationEditForm, certificationDataCounter)
			certificationaddForm = profile_certification_add_editForm()

			#extracurricularForm populate and edit
			exData = extracurricular_activities.objects.filter(user_id = User_obj)
			if len(exData) == 0:
				exData = 'unavailable'
				exInfoForm = None
			else:
				copy_exData = exData
				exDataCounter = range(len(copy_exData))
				exData = zip(copy_exData, exDataCounter)
				exEditForm = []
				for e in copy_exData:
					e_dict = {
						'tuple_id': e.id,
						'year': e.year,
						'activity_type': e.activity_type,
						'title': e.title,
						'details': e.activity_details,
						'organization': e.organization,
						'link': e.link					
					}			
					wl = profile_extracurricular_add_editForm(e_dict)
					exEditForm.append(wl)
				exInfoForm = zip(exEditForm, exDataCounter)
			extracurricularaddForm = profile_extracurricular_add_editForm()

			#achievementForm populate and edit
			achData = achievements.objects.filter(user_id = User_obj)
			if len(achData) == 0:
				achData = 'unavailable'
				achInfoForm = None
			else:
				copy_achData = achData
				achDataCounter = range(len(copy_achData))
				achData = zip(copy_achData, achDataCounter)
				achEditForm = []
				for a in copy_achData:
					a_dict = {
						'tuple_id': a.id,
						'year': a.year,
						'achievement_type': a.achievement_type,
						'title': a.title,
						'details': a.details,
						'organization': a.organization,
						'link': a.link					
					}			
					wl = profile_achievements_add_editForm(a_dict)
					achEditForm.append(wl)
				achInfoForm = zip(achEditForm, achDataCounter)
			achievementsaddForm = profile_achievements_add_editForm()

			#publicationForm populate and edit
			pubData = publication.objects.filter(user_id = User_obj)
			if len(pubData) == 0:
				pubData = 'unavailable'
				pubInfoForm = None
			else:
				copy_pubData = pubData
				pubDataCounter = range(len(copy_pubData))
				pubData = zip(copy_pubData, pubDataCounter)
				pubEditForm = []
				for p in copy_pubData:
					p_dict = {
						'tuple_id': p.id,
						'year': p.year,
						'mode': p.mode,
						'journal': p.journal,
						'status': p.status,				
						'details': p.details,					
						'link': p.link					
					}			
					wl = profile_publications_add_editForm(p_dict)
					pubEditForm.append(wl)
				pubInfoForm = zip(pubEditForm, pubDataCounter)
			publicationaddForm = profile_publications_add_editForm()

			#patentForm populate and edit
			patData = patent.objects.filter(user_id = User_obj)
			if len(patData) == 0:
				patData = 'unavailable'
				patInfoForm = None
			else:
				copy_patData = patData
				patDataCounter = range(len(copy_patData))
				patData = zip(copy_patData, patDataCounter)
				patEditForm = []
				for pa in copy_patData:
					pa_dict = {
						'tuple_id': pa.id,
						'year': pa.year,
						'mode': pa.mode,					
						'status': pa.patent_status,				
						'details': pa.patent_details
					}			
					wl = profile_patent_add_editForm(pa_dict)
					patEditForm.append(wl)
				patInfoForm = zip(patEditForm, patDataCounter)
			patentaddForm = profile_patent_add_editForm()

			skillsData = skills.objects.filter(user_id = User_obj)
			if len(skillsData) == 0:
				skillsData = 'unavailable'
				skillsInfoForm = None
			else:
				counter = 1
				skill_name_text = ''
				for s in skillsData:
					if counter == 1:
						skill_name_text = s.skill_name
					else:
						skill_name_text = skill_name_text + ',' + s.skill_name
					counter = counter + 1

				s_dict = {
					'skill': skill_name_text
				}
				skillsInfoForm = profile_skills_add_editForm(s_dict)
			skillsaddForm = profile_skills_add_editForm()

			variables = RequestContext(request, {
				'workForm': workForm,
				'educationForm': educationForm,
				'certificationForm': certificationForm,
				'publicationForm': publicationForm,
				'extracurricularForm': extracurricularForm,
				'patentForm': patentForm,
				'achievementForm': achievementForm,
				'aboutForm': aboutForm,
				'educationaddForm': educationaddForm,
				'workaddForm': workaddForm,
				'extracurricularaddForm': extracurricularaddForm,
				'certificationaddForm': certificationaddForm,
				'achievementsaddForm': achievementsaddForm,
				'publicationaddForm': publicationaddForm,
				'patentaddForm': patentaddForm,
				'aboutData': aboutData_existing,
				'educationData': educationData,	
				'educationInfoForm': educationInfoForm,
				'workData': workData,
				'workInfoForm': workInfoForm,
				'certificationData': certificationData,
				'certificationInfoForm': certificationInfoForm,
				'exData': exData,
				'exInfoForm': exInfoForm,
				'achData': achData,
				'achInfoForm': achInfoForm,
				'pubData': pubData,
				'pubInfoForm': pubInfoForm,
				'patData': patData,
				'patInfoForm': patInfoForm,
				'skillsaddForm': skillsaddForm,
				'skillsData': skillsData,
				'skillsInfoForm': skillsInfoForm,
				't_educationData': t_educationData,
				't_workData': t_workData,
				't_certificationData': t_certificationData,
				't_extracurricularData': t_extracurricularData,
				't_achievementData': t_achievementData,
				't_publicationData': t_publicationData,
				't_patentData': t_patentData
			})
			return render_to_response('profile-page.html', variables)

	elif request.method=='GET' and 'certificationdeleteForm' in request.GET:
		certificationaddForm = profile_certification_add_editForm(request.GET)
		if certificationaddForm.is_valid():
			row_id = certificationaddForm.cleaned_data['tuple_id']
			# year = certificationaddForm.cleaned_data['year']
			# agency = certificationaddForm.cleaned_data['agency']
			# mode = certificationaddForm.cleaned_data['mode']
			# details = certificationaddForm.cleaned_data['details']
			# attached_file = request.FILES['attach_file']

			certification_obj = certification.objects.get(id = row_id)
			
			certification_obj.delete()
			status = {
				'error': False,
				'error_message': '',
				'success': True,
				'success_message': 'Certification details deleted.',
			}
			workForm = profile_workForm()
			educationForm = profile_educationForm()
			certificationForm = profile_certificationForm()
			publicationForm = profile_publicationForm()
			extracurricularForm = profile_extracurricularForm()
			patentForm = profile_patentForm()
			achievementForm = profile_achievementForm()
			if len(t_educationData) == 0:
				t_educationData = 'unavailable'
			else:
				t_educationData = zip(t_educationData, range(len(t_educationData)))
			t_workData = work.objects.filter(user_id = User_obj)
			if len(t_workData) == 0:
				t_workData = 'unavailable'
			else:
				t_workData = zip(t_workData, range(len(t_workData)))
			t_certificationData = certification.objects.filter(user_id = User_obj)
			if len(t_certificationData) == 0:
				t_certificationData = 'unavailable'
			else:
				t_certificationData = zip(t_certificationData, range(len(t_certificationData)))
			t_extracurricularData = extracurricular_activities.objects.filter(user_id = User_obj)
			if len(t_extracurricularData) == 0:
				t_extracurricularData = 'unavailable'
			else:
				t_extracurricularData = zip(t_extracurricularData, range(len(t_extracurricularData)))
			t_achievementData = achievements.objects.filter(user_id = User_obj)
			if len(t_achievementData) == 0:
				t_achievementData = 'unavailable'
			else:
				t_achievementData = zip(t_achievementData, range(len(t_achievementData)))
			t_publicationData = publication.objects.filter(user_id = User_obj)
			if len(t_publicationData) == 0:
				t_publicationData = 'unavailable'
			else:
				t_publicationData = zip(t_publicationData, range(len(t_publicationData)))
			t_patentData = patent.objects.filter(user_id = User_obj)					
			if len(t_patentData) == 0:
				t_patentData = 'unavailable'
			else:
				t_patentData = zip(t_patentData, range(len(t_patentData)))


			
			# aboutForm population
			try:
				existing_about = user_details.objects.get(user_id = User_obj)
			except:
				existing_about = 'unavailable'
			if existing_about!='unavailable':
				aboutForm_existing = {
					'profession': existing_about.profession,
					'first_name': existing_about.first_name,
					'last_name': existing_about.last_name,
					'dob': existing_about.dob,
					'short_bio': existing_about.short_bio,
					'facebook_url': existing_about.facebook_url,
					'twitter_handle': existing_about.twitter_handle,
					'linkedin_url': existing_about.linkedin_url
				}
			else:
				aboutForm_existing = None
			aboutData_existing = aboutForm_existing
			aboutForm = profile_aboutmeForm(aboutForm_existing)

			#educationForm population and edit
			educationData = education.objects.filter(user_id = User_obj)
			if len(educationData) == 0:
				educationData = 'unavailable'
				educationInfoForm = None
			else:
				copy_educationData = educationData
				educationDataCounter = range(len(copy_educationData))
				educationData = zip(copy_educationData, educationDataCounter)
				educationEditForm = []
				for e in copy_educationData:
					e_dict = {
						'tuple_id': e.id,
						'year': e.year,
						'education_type': e.education_type,
						'institution': e.institution_name,
						'aggregate': e.aggregate,
						'what_did_you_do_there': e.what_did_you_do_there
					}
					el = profile_education_add_editForm(e_dict)
					educationEditForm.append(el)
				educationInfoForm = zip(educationEditForm, educationDataCounter)
			educationaddForm = profile_education_add_editForm()

			#workForm population and edit
			workData = work.objects.filter(user_id = User_obj)
			if len(workData) == 0:
				workData = 'unavailable'
				workInfoForm = None
			else:
				copy_workData = workData
				workDataCounter = range(len(copy_workData))
				workData = zip(copy_workData, workDataCounter)
				workEditForm = []
				for w in copy_workData:
					if w.work_type == 'Internship':
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'internship_company_name': w.internship_company_name,
							'internship_from_date': w.internship_date_from,
							'internship_to_date': w.internship_date_to,
							'internship_title': w.internship_title
						}
					elif w.work_type == 'Job':
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'job_company_name': w.job_company_name,
							'job_designation': w.job_designation,
							'job_from_date': w.job_date_from,
							'job_to_date': w.job_date_to
						}
					else:
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'freelancer_client': w.freelancer_client_name,
							'freelancer_project_title': w.freelancer_project_title,
							'freelancer_link': w.freelancer_link,
							'freelancer_project_status': w.freelancer_status,
							'freelancer_year': w.freelancer_year
						}
					wl = profile_work_add_editForm(w_dict)
					workEditForm.append(wl)
				workInfoForm = zip(workEditForm, workDataCounter)
			workaddForm = profile_work_add_editForm()

			#certificationForm populate and edit
			certificationData = certification.objects.filter(user_id = User_obj)
			if len(certificationData) == 0:
				certificationData = 'unavailable'
				certificationInfoForm = None
			else:
				copy_certificationData = certificationData
				certificationDataCounter = range(len(copy_certificationData))
				certificationData = zip(copy_certificationData, certificationDataCounter)
				certificationEditForm = []
				for c in copy_certificationData:
					c_dict = {
						'tuple_id': c.id,
						'year': c.year,
						'agency': c.agency,
						'mode': c.mode_of_certification,
						'details': c.details,					
					}		
					wl = profile_certification_add_editForm(c_dict)
					certificationEditForm.append(wl)
				certificationInfoForm = zip(certificationEditForm, certificationDataCounter)
			certificationaddForm = profile_certification_add_editForm()

			#extracurricularForm populate and edit
			exData = extracurricular_activities.objects.filter(user_id = User_obj)
			if len(exData) == 0:
				exData = 'unavailable'
				exInfoForm = None
			else:
				copy_exData = exData
				exDataCounter = range(len(copy_exData))
				exData = zip(copy_exData, exDataCounter)
				exEditForm = []
				for e in copy_exData:
					e_dict = {
						'tuple_id': e.id,
						'year': e.year,
						'activity_type': e.activity_type,
						'title': e.title,
						'details': e.activity_details,
						'organization': e.organization,
						'link': e.link					
					}			
					wl = profile_extracurricular_add_editForm(e_dict)
					exEditForm.append(wl)
				exInfoForm = zip(exEditForm, exDataCounter)
			extracurricularaddForm = profile_extracurricular_add_editForm()

			#achievementForm populate and edit
			achData = achievements.objects.filter(user_id = User_obj)
			if len(achData) == 0:
				achData = 'unavailable'
				achInfoForm = None
			else:
				copy_achData = achData
				achDataCounter = range(len(copy_achData))
				achData = zip(copy_achData, achDataCounter)
				achEditForm = []
				for a in copy_achData:
					a_dict = {
						'tuple_id': a.id,
						'year': a.year,
						'achievement_type': a.achievement_type,
						'title': a.title,
						'details': a.details,
						'organization': a.organization,
						'link': a.link					
					}			
					wl = profile_achievements_add_editForm(a_dict)
					achEditForm.append(wl)
				achInfoForm = zip(achEditForm, achDataCounter)
			achievementsaddForm = profile_achievements_add_editForm()

			#publicationForm populate and edit
			pubData = publication.objects.filter(user_id = User_obj)
			if len(pubData) == 0:
				pubData = 'unavailable'
				pubInfoForm = None
			else:
				copy_pubData = pubData
				pubDataCounter = range(len(copy_pubData))
				pubData = zip(copy_pubData, pubDataCounter)
				pubEditForm = []
				for p in copy_pubData:
					p_dict = {
						'tuple_id': p.id,
						'year': p.year,
						'mode': p.mode,
						'journal': p.journal,
						'status': p.status,				
						'details': p.details,					
						'link': p.link					
					}			
					wl = profile_publications_add_editForm(p_dict)
					pubEditForm.append(wl)
				pubInfoForm = zip(pubEditForm, pubDataCounter)
			publicationaddForm = profile_publications_add_editForm()

			#patentForm populate and edit
			patData = patent.objects.filter(user_id = User_obj)
			if len(patData) == 0:
				patData = 'unavailable'
				patInfoForm = None
			else:
				copy_patData = patData
				patDataCounter = range(len(copy_patData))
				patData = zip(copy_patData, patDataCounter)
				patEditForm = []
				for pa in copy_patData:
					pa_dict = {
						'tuple_id': pa.id,
						'year': pa.year,
						'mode': pa.mode,					
						'status': pa.patent_status,				
						'details': pa.patent_details
					}			
					wl = profile_patent_add_editForm(pa_dict)
					patEditForm.append(wl)
				patInfoForm = zip(patEditForm, patDataCounter)
			patentaddForm = profile_patent_add_editForm()

			skillsData = skills.objects.filter(user_id = User_obj)
			if len(skillsData) == 0:
				skillsData = 'unavailable'
				skillsInfoForm = None
			else:
				counter = 1
				skill_name_text = ''
				for s in skillsData:
					if counter == 1:
						skill_name_text = s.skill_name
					else:
						skill_name_text = skill_name_text + ',' + s.skill_name
					counter = counter + 1

				s_dict = {
					'skill': skill_name_text
				}
				skillsInfoForm = profile_skills_add_editForm(s_dict)
			skillsaddForm = profile_skills_add_editForm()

			variables = RequestContext(request, {
				'workForm': workForm,
				'educationForm': educationForm,
				'certificationForm': certificationForm,
				'publicationForm': publicationForm,
				'extracurricularForm': extracurricularForm,
				'patentForm': patentForm,
				'achievementForm': achievementForm,
				'aboutForm': aboutForm,
				'educationaddForm': educationaddForm,
				'workaddForm': workaddForm,
				'extracurricularaddForm': extracurricularaddForm,
				'certificationaddForm': certificationaddForm,
				'achievementsaddForm': achievementsaddForm,
				'publicationaddForm': publicationaddForm,
				'patentaddForm': patentaddForm,
				'aboutData': aboutData_existing,
				'educationData': educationData,	
				'educationInfoForm': educationInfoForm,
				'workData': workData,
				'workInfoForm': workInfoForm,
				'certificationData': certificationData,
				'certificationInfoForm': certificationInfoForm,
				'exData': exData,
				'exInfoForm': exInfoForm,
				'achData': achData,
				'achInfoForm': achInfoForm,
				'pubData': pubData,
				'pubInfoForm': pubInfoForm,
				'patData': patData,
				'patInfoForm': patInfoForm,
				'skillsaddForm': skillsaddForm,
				'skillsData': skillsData,
				'skillsInfoForm': skillsInfoForm,
				't_educationData': t_educationData,
				't_workData': t_workData,
				't_certificationData': t_certificationData,
				't_extracurricularData': t_extracurricularData,
				't_achievementData': t_achievementData,
				't_publicationData': t_publicationData,
				't_patentData': t_patentData
			})
			return render_to_response('profile-page.html', variables)

	elif request.method=='GET' and 'publicationaddForm' in request.GET:
		publicationaddForm = profile_publications_add_editForm(request.GET)
		if publicationaddForm.is_valid():
			year = publicationaddForm.cleaned_data['year']
			mode = publicationaddForm.cleaned_data['mode']
			journal = publicationaddForm.cleaned_data['journal']
			details = publicationaddForm.cleaned_data['details']
			status = publicationaddForm.cleaned_data['status']
			link = publicationaddForm.cleaned_data['link']

			publication_obj = publication(
				user_id = User_obj,
				year = year,
				mode = mode,
				journal = journal,
				details = details,
				status = status,
				link = link
			)
			publication_obj.save()
			status = {
				'error': False,
				'error_message': '',
				'success': True,
				'success_message': 'Publication details saved.',
			}
			workForm = profile_workForm()
			educationForm = profile_educationForm()
			certificationForm = profile_certificationForm()
			publicationForm = profile_publicationForm()
			extracurricularForm = profile_extracurricularForm()
			patentForm = profile_patentForm()
			achievementForm = profile_achievementForm()
			t_educationData = education.objects.filter(user_id = User_obj)
			if len(t_educationData) == 0:
				t_educationData = 'unavailable'
			else:
				t_educationData = zip(t_educationData, range(len(t_educationData)))
			t_workData = work.objects.filter(user_id = User_obj)
			if len(t_workData) == 0:
				t_workData = 'unavailable'
			else:
				t_workData = zip(t_workData, range(len(t_workData)))
			t_certificationData = certification.objects.filter(user_id = User_obj)
			if len(t_certificationData) == 0:
				t_certificationData = 'unavailable'
			else:
				t_certificationData = zip(t_certificationData, range(len(t_certificationData)))
			t_extracurricularData = extracurricular_activities.objects.filter(user_id = User_obj)
			if len(t_extracurricularData) == 0:
				t_extracurricularData = 'unavailable'
			else:
				t_extracurricularData = zip(t_extracurricularData, range(len(t_extracurricularData)))
			t_achievementData = achievements.objects.filter(user_id = User_obj)
			if len(t_achievementData) == 0:
				t_achievementData = 'unavailable'
			else:
				t_achievementData = zip(t_achievementData, range(len(t_achievementData)))
			t_publicationData = publication.objects.filter(user_id = User_obj)
			if len(t_publicationData) == 0:
				t_publicationData = 'unavailable'
			else:
				t_publicationData = zip(t_publicationData, range(len(t_publicationData)))
			t_patentData = patent.objects.filter(user_id = User_obj)					
			if len(t_patentData) == 0:
				t_patentData = 'unavailable'
			else:
				t_patentData = zip(t_patentData, range(len(t_patentData)))


			
			# aboutForm population
			try:
				existing_about = user_details.objects.get(user_id = User_obj)
			except:
				existing_about = 'unavailable'
			if existing_about!='unavailable':
				aboutForm_existing = {
					'profession': existing_about.profession,
					'first_name': existing_about.first_name,
					'last_name': existing_about.last_name,
					'dob': existing_about.dob,
					'short_bio': existing_about.short_bio,
					'facebook_url': existing_about.facebook_url,
					'twitter_handle': existing_about.twitter_handle,
					'linkedin_url': existing_about.linkedin_url
				}
			else:
				aboutForm_existing = None
			aboutData_existing = aboutForm_existing
			aboutForm = profile_aboutmeForm(aboutForm_existing)

			#educationForm population and edit
			educationData = education.objects.filter(user_id = User_obj)
			if len(educationData) == 0:
				educationData = 'unavailable'
				educationInfoForm = None
			else:
				copy_educationData = educationData
				educationDataCounter = range(len(copy_educationData))
				educationData = zip(copy_educationData, educationDataCounter)
				educationEditForm = []
				for e in copy_educationData:
					e_dict = {
						'tuple_id': e.id,
						'year': e.year,
						'education_type': e.education_type,
						'institution': e.institution_name,
						'aggregate': e.aggregate,
						'what_did_you_do_there': e.what_did_you_do_there
					}
					el = profile_education_add_editForm(e_dict)
					educationEditForm.append(el)
				educationInfoForm = zip(educationEditForm, educationDataCounter)
			educationaddForm = profile_education_add_editForm()

			#workForm population and edit
			workData = work.objects.filter(user_id = User_obj)
			if len(workData) == 0:
				workData = 'unavailable'
				workInfoForm = None
			else:
				copy_workData = workData
				workDataCounter = range(len(copy_workData))
				workData = zip(copy_workData, workDataCounter)
				workEditForm = []
				for w in copy_workData:
					if w.work_type == 'Internship':
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'internship_company_name': w.internship_company_name,
							'internship_from_date': w.internship_date_from,
							'internship_to_date': w.internship_date_to,
							'internship_title': w.internship_title
						}
					elif w.work_type == 'Job':
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'job_company_name': w.job_company_name,
							'job_designation': w.job_designation,
							'job_from_date': w.job_date_from,
							'job_to_date': w.job_date_to
						}
					else:
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'freelancer_client': w.freelancer_client_name,
							'freelancer_project_title': w.freelancer_project_title,
							'freelancer_link': w.freelancer_link,
							'freelancer_project_status': w.freelancer_status,
							'freelancer_year': w.freelancer_year
						}
					wl = profile_work_add_editForm(w_dict)
					workEditForm.append(wl)
				workInfoForm = zip(workEditForm, workDataCounter)
			workaddForm = profile_work_add_editForm()

			#certificationForm populate and edit
			certificationData = certification.objects.filter(user_id = User_obj)
			if len(certificationData) == 0:
				certificationData = 'unavailable'
				certificationInfoForm = None
			else:
				copy_certificationData = certificationData
				certificationDataCounter = range(len(copy_certificationData))
				certificationData = zip(copy_certificationData, certificationDataCounter)
				certificationEditForm = []
				for c in copy_certificationData:
					c_dict = {
						'tuple_id': c.id,
						'year': c.year,
						'agency': c.agency,
						'mode': c.mode_of_certification,
						'details': c.details,					
					}		
					wl = profile_certification_add_editForm(c_dict)
					certificationEditForm.append(wl)
				certificationInfoForm = zip(certificationEditForm, certificationDataCounter)
			certificationaddForm = profile_certification_add_editForm()

			#extracurricularForm populate and edit
			exData = extracurricular_activities.objects.filter(user_id = User_obj)
			if len(exData) == 0:
				exData = 'unavailable'
				exInfoForm = None
			else:
				copy_exData = exData
				exDataCounter = range(len(copy_exData))
				exData = zip(copy_exData, exDataCounter)
				exEditForm = []
				for e in copy_exData:
					e_dict = {
						'tuple_id': e.id,
						'year': e.year,
						'activity_type': e.activity_type,
						'title': e.title,
						'details': e.activity_details,
						'organization': e.organization,
						'link': e.link					
					}			
					wl = profile_extracurricular_add_editForm(e_dict)
					exEditForm.append(wl)
				exInfoForm = zip(exEditForm, exDataCounter)
			extracurricularaddForm = profile_extracurricular_add_editForm()

			#achievementForm populate and edit
			achData = achievements.objects.filter(user_id = User_obj)
			if len(achData) == 0:
				achData = 'unavailable'
				achInfoForm = None
			else:
				copy_achData = achData
				achDataCounter = range(len(copy_achData))
				achData = zip(copy_achData, achDataCounter)
				achEditForm = []
				for a in copy_achData:
					a_dict = {
						'tuple_id': a.id,
						'year': a.year,
						'achievement_type': a.achievement_type,
						'title': a.title,
						'details': a.details,
						'organization': a.organization,
						'link': a.link					
					}			
					wl = profile_achievements_add_editForm(a_dict)
					achEditForm.append(wl)
				achInfoForm = zip(achEditForm, achDataCounter)
			achievementsaddForm = profile_achievements_add_editForm()

			#publicationForm populate and edit
			pubData = publication.objects.filter(user_id = User_obj)
			if len(pubData) == 0:
				pubData = 'unavailable'
				pubInfoForm = None
			else:
				copy_pubData = pubData
				pubDataCounter = range(len(copy_pubData))
				pubData = zip(copy_pubData, pubDataCounter)
				pubEditForm = []
				for p in copy_pubData:
					p_dict = {
						'tuple_id': p.id,
						'year': p.year,
						'mode': p.mode,
						'journal': p.journal,
						'status': p.status,				
						'details': p.details,					
						'link': p.link					
					}			
					wl = profile_publications_add_editForm(p_dict)
					pubEditForm.append(wl)
				pubInfoForm = zip(pubEditForm, pubDataCounter)
			publicationaddForm = profile_publications_add_editForm()

			#patentForm populate and edit
			patData = patent.objects.filter(user_id = User_obj)
			if len(patData) == 0:
				patData = 'unavailable'
				patInfoForm = None
			else:
				copy_patData = patData
				patDataCounter = range(len(copy_patData))
				patData = zip(copy_patData, patDataCounter)
				patEditForm = []
				for pa in copy_patData:
					pa_dict = {
						'tuple_id': pa.id,
						'year': pa.year,
						'mode': pa.mode,					
						'status': pa.patent_status,				
						'details': pa.patent_details
					}			
					wl = profile_patent_add_editForm(pa_dict)
					patEditForm.append(wl)
				patInfoForm = zip(patEditForm, patDataCounter)
			patentaddForm = profile_patent_add_editForm()

			skillsData = skills.objects.filter(user_id = User_obj)
			if len(skillsData) == 0:
				skillsData = 'unavailable'
				skillsInfoForm = None
			else:
				counter = 1
				skill_name_text = ''
				for s in skillsData:
					if counter == 1:
						skill_name_text = s.skill_name
					else:
						skill_name_text = skill_name_text + ',' + s.skill_name
					counter = counter + 1

				s_dict = {
					'skill': skill_name_text
				}
				skillsInfoForm = profile_skills_add_editForm(s_dict)
			skillsaddForm = profile_skills_add_editForm()

			variables = RequestContext(request, {
				'workForm': workForm,
				'educationForm': educationForm,
				'certificationForm': certificationForm,
				'publicationForm': publicationForm,
				'extracurricularForm': extracurricularForm,
				'patentForm': patentForm,
				'achievementForm': achievementForm,
				'aboutForm': aboutForm,
				'educationaddForm': educationaddForm,
				'workaddForm': workaddForm,
				'extracurricularaddForm': extracurricularaddForm,
				'certificationaddForm': certificationaddForm,
				'achievementsaddForm': achievementsaddForm,
				'publicationaddForm': publicationaddForm,
				'patentaddForm': patentaddForm,
				'aboutData': aboutData_existing,
				'educationData': educationData,	
				'educationInfoForm': educationInfoForm,
				'workData': workData,
				'workInfoForm': workInfoForm,
				'certificationData': certificationData,
				'certificationInfoForm': certificationInfoForm,
				'exData': exData,
				'exInfoForm': exInfoForm,
				'achData': achData,
				'achInfoForm': achInfoForm,
				'pubData': pubData,
				'pubInfoForm': pubInfoForm,
				'patData': patData,
				'patInfoForm': patInfoForm,
				'skillsaddForm': skillsaddForm,
				'skillsData': skillsData,
				'skillsInfoForm': skillsInfoForm,
				't_educationData': t_educationData,
				't_workData': t_workData,
				't_certificationData': t_certificationData,
				't_extracurricularData': t_extracurricularData,
				't_achievementData': t_achievementData,
				't_publicationData': t_publicationData,
				't_patentData': t_patentData
			})
			return render_to_response('profile-page.html', variables)

	elif request.method=='GET' and 'publicationeditForm' in request.GET:
		publicationaddForm = profile_publications_add_editForm(request.GET)
		if publicationaddForm.is_valid():
			row_id = publicationaddForm.cleaned_data['tuple_id']
			year = publicationaddForm.cleaned_data['year']
			mode = publicationaddForm.cleaned_data['mode']
			journal = publicationaddForm.cleaned_data['journal']
			details = publicationaddForm.cleaned_data['details']
			status = publicationaddForm.cleaned_data['status']
			link = publicationaddForm.cleaned_data['link']

			publication_obj = publication.objects.get(id = row_id)

			publication_obj.year = year
			publication_obj.mode = mode
			publication_obj.journal = journal
			publication_obj.details = details
			publication_obj.status = status
			publication_obj.link = link

			publication_obj.save()

			status = {
				'error': False,
				'error_message': '',
				'success': True,
				'success_message': 'Publication details saved.',
			}
			workForm = profile_workForm()
			educationForm = profile_educationForm()
			certificationForm = profile_certificationForm()
			publicationForm = profile_publicationForm()
			extracurricularForm = profile_extracurricularForm()
			patentForm = profile_patentForm()
			achievementForm = profile_achievementForm()
			t_educationData = education.objects.filter(user_id = User_obj)
			if len(t_educationData) == 0:
				t_educationData = 'unavailable'
			else:
				t_educationData = zip(t_educationData, range(len(t_educationData)))
			t_workData = work.objects.filter(user_id = User_obj)
			if len(t_workData) == 0:
				t_workData = 'unavailable'
			else:
				t_workData = zip(t_workData, range(len(t_workData)))
			t_certificationData = certification.objects.filter(user_id = User_obj)
			if len(t_certificationData) == 0:
				t_certificationData = 'unavailable'
			else:
				t_certificationData = zip(t_certificationData, range(len(t_certificationData)))
			t_extracurricularData = extracurricular_activities.objects.filter(user_id = User_obj)
			if len(t_extracurricularData) == 0:
				t_extracurricularData = 'unavailable'
			else:
				t_extracurricularData = zip(t_extracurricularData, range(len(t_extracurricularData)))
			t_achievementData = achievements.objects.filter(user_id = User_obj)
			if len(t_achievementData) == 0:
				t_achievementData = 'unavailable'
			else:
				t_achievementData = zip(t_achievementData, range(len(t_achievementData)))
			t_publicationData = publication.objects.filter(user_id = User_obj)
			if len(t_publicationData) == 0:
				t_publicationData = 'unavailable'
			else:
				t_publicationData = zip(t_publicationData, range(len(t_publicationData)))
			t_patentData = patent.objects.filter(user_id = User_obj)					
			if len(t_patentData) == 0:
				t_patentData = 'unavailable'
			else:
				t_patentData = zip(t_patentData, range(len(t_patentData)))


			
			# aboutForm population
			try:
				existing_about = user_details.objects.get(user_id = User_obj)
			except:
				existing_about = 'unavailable'
			if existing_about!='unavailable':
				aboutForm_existing = {
					'profession': existing_about.profession,
					'first_name': existing_about.first_name,
					'last_name': existing_about.last_name,
					'dob': existing_about.dob,
					'short_bio': existing_about.short_bio,
					'facebook_url': existing_about.facebook_url,
					'twitter_handle': existing_about.twitter_handle,
					'linkedin_url': existing_about.linkedin_url
				}
			else:
				aboutForm_existing = None
			aboutData_existing = aboutForm_existing
			aboutForm = profile_aboutmeForm(aboutForm_existing)

			#educationForm population and edit
			educationData = education.objects.filter(user_id = User_obj)
			if len(educationData) == 0:
				educationData = 'unavailable'
				educationInfoForm = None
			else:
				copy_educationData = educationData
				educationDataCounter = range(len(copy_educationData))
				educationData = zip(copy_educationData, educationDataCounter)
				educationEditForm = []
				for e in copy_educationData:
					e_dict = {
						'tuple_id': e.id,
						'year': e.year,
						'education_type': e.education_type,
						'institution': e.institution_name,
						'aggregate': e.aggregate,
						'what_did_you_do_there': e.what_did_you_do_there
					}
					el = profile_education_add_editForm(e_dict)
					educationEditForm.append(el)
				educationInfoForm = zip(educationEditForm, educationDataCounter)
			educationaddForm = profile_education_add_editForm()

			#workForm population and edit
			workData = work.objects.filter(user_id = User_obj)
			if len(workData) == 0:
				workData = 'unavailable'
				workInfoForm = None
			else:
				copy_workData = workData
				workDataCounter = range(len(copy_workData))
				workData = zip(copy_workData, workDataCounter)
				workEditForm = []
				for w in copy_workData:
					if w.work_type == 'Internship':
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'internship_company_name': w.internship_company_name,
							'internship_from_date': w.internship_date_from,
							'internship_to_date': w.internship_date_to,
							'internship_title': w.internship_title
						}
					elif w.work_type == 'Job':
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'job_company_name': w.job_company_name,
							'job_designation': w.job_designation,
							'job_from_date': w.job_date_from,
							'job_to_date': w.job_date_to
						}
					else:
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'freelancer_client': w.freelancer_client_name,
							'freelancer_project_title': w.freelancer_project_title,
							'freelancer_link': w.freelancer_link,
							'freelancer_project_status': w.freelancer_status,
							'freelancer_year': w.freelancer_year
						}
					wl = profile_work_add_editForm(w_dict)
					workEditForm.append(wl)
				workInfoForm = zip(workEditForm, workDataCounter)
			workaddForm = profile_work_add_editForm()

			#certificationForm populate and edit
			certificationData = certification.objects.filter(user_id = User_obj)
			if len(certificationData) == 0:
				certificationData = 'unavailable'
				certificationInfoForm = None
			else:
				copy_certificationData = certificationData
				certificationDataCounter = range(len(copy_certificationData))
				certificationData = zip(copy_certificationData, certificationDataCounter)
				certificationEditForm = []
				for c in copy_certificationData:
					c_dict = {
						'tuple_id': c.id,
						'year': c.year,
						'agency': c.agency,
						'mode': c.mode_of_certification,
						'details': c.details,					
					}		
					wl = profile_certification_add_editForm(c_dict)
					certificationEditForm.append(wl)
				certificationInfoForm = zip(certificationEditForm, certificationDataCounter)
			certificationaddForm = profile_certification_add_editForm()

			#extracurricularForm populate and edit
			exData = extracurricular_activities.objects.filter(user_id = User_obj)
			if len(exData) == 0:
				exData = 'unavailable'
				exInfoForm = None
			else:
				copy_exData = exData
				exDataCounter = range(len(copy_exData))
				exData = zip(copy_exData, exDataCounter)
				exEditForm = []
				for e in copy_exData:
					e_dict = {
						'tuple_id': e.id,
						'year': e.year,
						'activity_type': e.activity_type,
						'title': e.title,
						'details': e.activity_details,
						'organization': e.organization,
						'link': e.link					
					}			
					wl = profile_extracurricular_add_editForm(e_dict)
					exEditForm.append(wl)
				exInfoForm = zip(exEditForm, exDataCounter)
			extracurricularaddForm = profile_extracurricular_add_editForm()

			#achievementForm populate and edit
			achData = achievements.objects.filter(user_id = User_obj)
			if len(achData) == 0:
				achData = 'unavailable'
				achInfoForm = None
			else:
				copy_achData = achData
				achDataCounter = range(len(copy_achData))
				achData = zip(copy_achData, achDataCounter)
				achEditForm = []
				for a in copy_achData:
					a_dict = {
						'tuple_id': a.id,
						'year': a.year,
						'achievement_type': a.achievement_type,
						'title': a.title,
						'details': a.details,
						'organization': a.organization,
						'link': a.link					
					}			
					wl = profile_achievements_add_editForm(a_dict)
					achEditForm.append(wl)
				achInfoForm = zip(achEditForm, achDataCounter)
			achievementsaddForm = profile_achievements_add_editForm()

			#publicationForm populate and edit
			pubData = publication.objects.filter(user_id = User_obj)
			if len(pubData) == 0:
				pubData = 'unavailable'
				pubInfoForm = None
			else:
				copy_pubData = pubData
				pubDataCounter = range(len(copy_pubData))
				pubData = zip(copy_pubData, pubDataCounter)
				pubEditForm = []
				for p in copy_pubData:
					p_dict = {
						'tuple_id': p.id,
						'year': p.year,
						'mode': p.mode,
						'journal': p.journal,
						'status': p.status,				
						'details': p.details,					
						'link': p.link					
					}			
					wl = profile_publications_add_editForm(p_dict)
					pubEditForm.append(wl)
				pubInfoForm = zip(pubEditForm, pubDataCounter)
			publicationaddForm = profile_publications_add_editForm()

			#patentForm populate and edit
			patData = patent.objects.filter(user_id = User_obj)
			if len(patData) == 0:
				patData = 'unavailable'
				patInfoForm = None
			else:
				copy_patData = patData
				patDataCounter = range(len(copy_patData))
				patData = zip(copy_patData, patDataCounter)
				patEditForm = []
				for pa in copy_patData:
					pa_dict = {
						'tuple_id': pa.id,
						'year': pa.year,
						'mode': pa.mode,					
						'status': pa.patent_status,				
						'details': pa.patent_details
					}			
					wl = profile_patent_add_editForm(pa_dict)
					patEditForm.append(wl)
				patInfoForm = zip(patEditForm, patDataCounter)
			patentaddForm = profile_patent_add_editForm()

			skillsData = skills.objects.filter(user_id = User_obj)
			if len(skillsData) == 0:
				skillsData = 'unavailable'
				skillsInfoForm = None
			else:
				counter = 1
				skill_name_text = ''
				for s in skillsData:
					if counter == 1:
						skill_name_text = s.skill_name
					else:
						skill_name_text = skill_name_text + ',' + s.skill_name
					counter = counter + 1

				s_dict = {
					'skill': skill_name_text
				}
				skillsInfoForm = profile_skills_add_editForm(s_dict)
			skillsaddForm = profile_skills_add_editForm()

			variables = RequestContext(request, {
				'workForm': workForm,
				'educationForm': educationForm,
				'certificationForm': certificationForm,
				'publicationForm': publicationForm,
				'extracurricularForm': extracurricularForm,
				'patentForm': patentForm,
				'achievementForm': achievementForm,
				'aboutForm': aboutForm,
				'educationaddForm': educationaddForm,
				'workaddForm': workaddForm,
				'extracurricularaddForm': extracurricularaddForm,
				'certificationaddForm': certificationaddForm,
				'achievementsaddForm': achievementsaddForm,
				'publicationaddForm': publicationaddForm,
				'patentaddForm': patentaddForm,
				'aboutData': aboutData_existing,
				'educationData': educationData,	
				'educationInfoForm': educationInfoForm,
				'workData': workData,
				'workInfoForm': workInfoForm,
				'certificationData': certificationData,
				'certificationInfoForm': certificationInfoForm,
				'exData': exData,
				'exInfoForm': exInfoForm,
				'achData': achData,
				'achInfoForm': achInfoForm,
				'pubData': pubData,
				'pubInfoForm': pubInfoForm,
				'patData': patData,
				'patInfoForm': patInfoForm,
				'skillsaddForm': skillsaddForm,
				'skillsData': skillsData,
				'skillsInfoForm': skillsInfoForm,
				't_educationData': t_educationData,
				't_workData': t_workData,
				't_certificationData': t_certificationData,
				't_extracurricularData': t_extracurricularData,
				't_achievementData': t_achievementData,
				't_publicationData': t_publicationData,
				't_patentData': t_patentData
			})
			return render_to_response('profile-page.html', variables)

	elif request.method=='GET' and 'publicationdeleteForm' in request.GET:
		publicationaddForm = profile_publications_add_editForm(request.GET)
		if publicationaddForm.is_valid():
			row_id = publicationaddForm.cleaned_data['tuple_id']
			# year = publicationaddForm.cleaned_data['year']
			# mode = publicationaddForm.cleaned_data['mode']
			# journal = publicationaddForm.cleaned_data['journal']
			# details = publicationaddForm.cleaned_data['details']
			# status = publicationaddForm.cleaned_data['status']
			# link = publicationaddForm.cleaned_data['link']

			publication_obj = publication.objects.get(id = row_id)

			publication_obj.delete()

			status = {
				'error': False,
				'error_message': '',
				'success': True,
				'success_message': 'Publication details deleted.',
			}
			workForm = profile_workForm()
			educationForm = profile_educationForm()
			certificationForm = profile_certificationForm()
			publicationForm = profile_publicationForm()
			extracurricularForm = profile_extracurricularForm()
			patentForm = profile_patentForm()
			achievementForm = profile_achievementForm()
			t_educationData = education.objects.filter(user_id = User_obj)
			if len(t_educationData) == 0:
				t_educationData = 'unavailable'
			else:
				t_educationData = zip(t_educationData, range(len(t_educationData)))
			t_workData = work.objects.filter(user_id = User_obj)
			if len(t_workData) == 0:
				t_workData = 'unavailable'
			else:
				t_workData = zip(t_workData, range(len(t_workData)))
			t_certificationData = certification.objects.filter(user_id = User_obj)
			if len(t_certificationData) == 0:
				t_certificationData = 'unavailable'
			else:
				t_certificationData = zip(t_certificationData, range(len(t_certificationData)))
			t_extracurricularData = extracurricular_activities.objects.filter(user_id = User_obj)
			if len(t_extracurricularData) == 0:
				t_extracurricularData = 'unavailable'
			else:
				t_extracurricularData = zip(t_extracurricularData, range(len(t_extracurricularData)))
			t_achievementData = achievements.objects.filter(user_id = User_obj)
			if len(t_achievementData) == 0:
				t_achievementData = 'unavailable'
			else:
				t_achievementData = zip(t_achievementData, range(len(t_achievementData)))
			t_publicationData = publication.objects.filter(user_id = User_obj)
			if len(t_publicationData) == 0:
				t_publicationData = 'unavailable'
			else:
				t_publicationData = zip(t_publicationData, range(len(t_publicationData)))
			t_patentData = patent.objects.filter(user_id = User_obj)					
			if len(t_patentData) == 0:
				t_patentData = 'unavailable'
			else:
				t_patentData = zip(t_patentData, range(len(t_patentData)))


			
			# aboutForm population
			try:
				existing_about = user_details.objects.get(user_id = User_obj)
			except:
				existing_about = 'unavailable'
			if existing_about!='unavailable':
				aboutForm_existing = {
					'profession': existing_about.profession,
					'first_name': existing_about.first_name,
					'last_name': existing_about.last_name,
					'dob': existing_about.dob,
					'short_bio': existing_about.short_bio,
					'facebook_url': existing_about.facebook_url,
					'twitter_handle': existing_about.twitter_handle,
					'linkedin_url': existing_about.linkedin_url
				}
			else:
				aboutForm_existing = None
			aboutData_existing = aboutForm_existing
			aboutForm = profile_aboutmeForm(aboutForm_existing)

			#educationForm population and edit
			educationData = education.objects.filter(user_id = User_obj)
			if len(educationData) == 0:
				educationData = 'unavailable'
				educationInfoForm = None
			else:
				copy_educationData = educationData
				educationDataCounter = range(len(copy_educationData))
				educationData = zip(copy_educationData, educationDataCounter)
				educationEditForm = []
				for e in copy_educationData:
					e_dict = {
						'tuple_id': e.id,
						'year': e.year,
						'education_type': e.education_type,
						'institution': e.institution_name,
						'aggregate': e.aggregate,
						'what_did_you_do_there': e.what_did_you_do_there
					}
					el = profile_education_add_editForm(e_dict)
					educationEditForm.append(el)
				educationInfoForm = zip(educationEditForm, educationDataCounter)
			educationaddForm = profile_education_add_editForm()

			#workForm population and edit
			workData = work.objects.filter(user_id = User_obj)
			if len(workData) == 0:
				workData = 'unavailable'
				workInfoForm = None
			else:
				copy_workData = workData
				workDataCounter = range(len(copy_workData))
				workData = zip(copy_workData, workDataCounter)
				workEditForm = []
				for w in copy_workData:
					if w.work_type == 'Internship':
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'internship_company_name': w.internship_company_name,
							'internship_from_date': w.internship_date_from,
							'internship_to_date': w.internship_date_to,
							'internship_title': w.internship_title
						}
					elif w.work_type == 'Job':
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'job_company_name': w.job_company_name,
							'job_designation': w.job_designation,
							'job_from_date': w.job_date_from,
							'job_to_date': w.job_date_to
						}
					else:
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'freelancer_client': w.freelancer_client_name,
							'freelancer_project_title': w.freelancer_project_title,
							'freelancer_link': w.freelancer_link,
							'freelancer_project_status': w.freelancer_status,
							'freelancer_year': w.freelancer_year
						}
					wl = profile_work_add_editForm(w_dict)
					workEditForm.append(wl)
				workInfoForm = zip(workEditForm, workDataCounter)
			workaddForm = profile_work_add_editForm()

			#certificationForm populate and edit
			certificationData = certification.objects.filter(user_id = User_obj)
			if len(certificationData) == 0:
				certificationData = 'unavailable'
				certificationInfoForm = None
			else:
				copy_certificationData = certificationData
				certificationDataCounter = range(len(copy_certificationData))
				certificationData = zip(copy_certificationData, certificationDataCounter)
				certificationEditForm = []
				for c in copy_certificationData:
					c_dict = {
						'tuple_id': c.id,
						'year': c.year,
						'agency': c.agency,
						'mode': c.mode_of_certification,
						'details': c.details,					
					}		
					wl = profile_certification_add_editForm(c_dict)
					certificationEditForm.append(wl)
				certificationInfoForm = zip(certificationEditForm, certificationDataCounter)
			certificationaddForm = profile_certification_add_editForm()

			#extracurricularForm populate and edit
			exData = extracurricular_activities.objects.filter(user_id = User_obj)
			if len(exData) == 0:
				exData = 'unavailable'
				exInfoForm = None
			else:
				copy_exData = exData
				exDataCounter = range(len(copy_exData))
				exData = zip(copy_exData, exDataCounter)
				exEditForm = []
				for e in copy_exData:
					e_dict = {
						'tuple_id': e.id,
						'year': e.year,
						'activity_type': e.activity_type,
						'title': e.title,
						'details': e.activity_details,
						'organization': e.organization,
						'link': e.link					
					}			
					wl = profile_extracurricular_add_editForm(e_dict)
					exEditForm.append(wl)
				exInfoForm = zip(exEditForm, exDataCounter)
			extracurricularaddForm = profile_extracurricular_add_editForm()

			#achievementForm populate and edit
			achData = achievements.objects.filter(user_id = User_obj)
			if len(achData) == 0:
				achData = 'unavailable'
				achInfoForm = None
			else:
				copy_achData = achData
				achDataCounter = range(len(copy_achData))
				achData = zip(copy_achData, achDataCounter)
				achEditForm = []
				for a in copy_achData:
					a_dict = {
						'tuple_id': a.id,
						'year': a.year,
						'achievement_type': a.achievement_type,
						'title': a.title,
						'details': a.details,
						'organization': a.organization,
						'link': a.link					
					}			
					wl = profile_achievements_add_editForm(a_dict)
					achEditForm.append(wl)
				achInfoForm = zip(achEditForm, achDataCounter)
			achievementsaddForm = profile_achievements_add_editForm()

			#publicationForm populate and edit
			pubData = publication.objects.filter(user_id = User_obj)
			if len(pubData) == 0:
				pubData = 'unavailable'
				pubInfoForm = None
			else:
				copy_pubData = pubData
				pubDataCounter = range(len(copy_pubData))
				pubData = zip(copy_pubData, pubDataCounter)
				pubEditForm = []
				for p in copy_pubData:
					p_dict = {
						'tuple_id': p.id,
						'year': p.year,
						'mode': p.mode,
						'journal': p.journal,
						'status': p.status,				
						'details': p.details,					
						'link': p.link					
					}			
					wl = profile_publications_add_editForm(p_dict)
					pubEditForm.append(wl)
				pubInfoForm = zip(pubEditForm, pubDataCounter)
			publicationaddForm = profile_publications_add_editForm()

			#patentForm populate and edit
			patData = patent.objects.filter(user_id = User_obj)
			if len(patData) == 0:
				patData = 'unavailable'
				patInfoForm = None
			else:
				copy_patData = patData
				patDataCounter = range(len(copy_patData))
				patData = zip(copy_patData, patDataCounter)
				patEditForm = []
				for pa in copy_patData:
					pa_dict = {
						'tuple_id': pa.id,
						'year': pa.year,
						'mode': pa.mode,					
						'status': pa.patent_status,				
						'details': pa.patent_details
					}			
					wl = profile_patent_add_editForm(pa_dict)
					patEditForm.append(wl)
				patInfoForm = zip(patEditForm, patDataCounter)
			patentaddForm = profile_patent_add_editForm()

			skillsData = skills.objects.filter(user_id = User_obj)
			if len(skillsData) == 0:
				skillsData = 'unavailable'
				skillsInfoForm = None
			else:
				counter = 1
				skill_name_text = ''
				for s in skillsData:
					if counter == 1:
						skill_name_text = s.skill_name
					else:
						skill_name_text = skill_name_text + ',' + s.skill_name
					counter = counter + 1

				s_dict = {
					'skill': skill_name_text
				}
				skillsInfoForm = profile_skills_add_editForm(s_dict)
			skillsaddForm = profile_skills_add_editForm()

			variables = RequestContext(request, {
				'workForm': workForm,
				'educationForm': educationForm,
				'certificationForm': certificationForm,
				'publicationForm': publicationForm,
				'extracurricularForm': extracurricularForm,
				'patentForm': patentForm,
				'achievementForm': achievementForm,
				'aboutForm': aboutForm,
				'educationaddForm': educationaddForm,
				'workaddForm': workaddForm,
				'extracurricularaddForm': extracurricularaddForm,
				'certificationaddForm': certificationaddForm,
				'achievementsaddForm': achievementsaddForm,
				'publicationaddForm': publicationaddForm,
				'patentaddForm': patentaddForm,
				'aboutData': aboutData_existing,
				'educationData': educationData,	
				'educationInfoForm': educationInfoForm,
				'workData': workData,
				'workInfoForm': workInfoForm,
				'certificationData': certificationData,
				'certificationInfoForm': certificationInfoForm,
				'exData': exData,
				'exInfoForm': exInfoForm,
				'achData': achData,
				'achInfoForm': achInfoForm,
				'pubData': pubData,
				'pubInfoForm': pubInfoForm,
				'patData': patData,
				'patInfoForm': patInfoForm,
				'skillsaddForm': skillsaddForm,
				'skillsData': skillsData,
				'skillsInfoForm': skillsInfoForm,
				't_educationData': t_educationData,
				't_workData': t_workData,
				't_certificationData': t_certificationData,
				't_extracurricularData': t_extracurricularData,
				't_achievementData': t_achievementData,
				't_publicationData': t_publicationData,
				't_patentData': t_patentData
			})
			return render_to_response('profile-page.html', variables)	

	elif request.method=='GET' and 'extracurricularaddForm' in request.GET:
		extracurricularaddForm = profile_extracurricular_add_editForm(request.GET)
		if extracurricularaddForm.is_valid():
			year = extracurricularaddForm.cleaned_data['year']
			activity_type = extracurricularaddForm.cleaned_data['activity_type']
			title = extracurricularaddForm.cleaned_data['title']
			details = extracurricularaddForm.cleaned_data['details']
			organization = extracurricularaddForm.cleaned_data['organization']
			link = extracurricularaddForm.cleaned_data['link']

			extracurricular_obj = extracurricular_activities(
				user_id = User_obj,
				year = year,
				activity_type = activity_type,
				activity_details = details,
				title = title,
				organization = organization,
				link = link
			)
			extracurricular_obj.save()
			status = {
				'error': False,
				'error_message': '',
				'success': True,
				'success_message': 'Extracurricular details saved.',
			}
			workForm = profile_workForm()
			educationForm = profile_educationForm()
			certificationForm = profile_certificationForm()
			publicationForm = profile_publicationForm()
			extracurricularForm = profile_extracurricularForm()
			patentForm = profile_patentForm()
			achievementForm = profile_achievementForm()
			t_educationData = education.objects.filter(user_id = User_obj)
			if len(t_educationData) == 0:
				t_educationData = 'unavailable'
			else:
				t_educationData = zip(t_educationData, range(len(t_educationData)))
			t_workData = work.objects.filter(user_id = User_obj)
			if len(t_workData) == 0:
				t_workData = 'unavailable'
			else:
				t_workData = zip(t_workData, range(len(t_workData)))
			t_certificationData = certification.objects.filter(user_id = User_obj)
			if len(t_certificationData) == 0:
				t_certificationData = 'unavailable'
			else:
				t_certificationData = zip(t_certificationData, range(len(t_certificationData)))
			t_extracurricularData = extracurricular_activities.objects.filter(user_id = User_obj)
			if len(t_extracurricularData) == 0:
				t_extracurricularData = 'unavailable'
			else:
				t_extracurricularData = zip(t_extracurricularData, range(len(t_extracurricularData)))
			t_achievementData = achievements.objects.filter(user_id = User_obj)
			if len(t_achievementData) == 0:
				t_achievementData = 'unavailable'
			else:
				t_achievementData = zip(t_achievementData, range(len(t_achievementData)))
			t_publicationData = publication.objects.filter(user_id = User_obj)
			if len(t_publicationData) == 0:
				t_publicationData = 'unavailable'
			else:
				t_publicationData = zip(t_publicationData, range(len(t_publicationData)))
			t_patentData = patent.objects.filter(user_id = User_obj)					
			if len(t_patentData) == 0:
				t_patentData = 'unavailable'
			else:
				t_patentData = zip(t_patentData, range(len(t_patentData)))


			
			# aboutForm population
			try:
				existing_about = user_details.objects.get(user_id = User_obj)
			except:
				existing_about = 'unavailable'
			if existing_about!='unavailable':
				aboutForm_existing = {
					'profession': existing_about.profession,
					'first_name': existing_about.first_name,
					'last_name': existing_about.last_name,
					'dob': existing_about.dob,
					'short_bio': existing_about.short_bio,
					'facebook_url': existing_about.facebook_url,
					'twitter_handle': existing_about.twitter_handle,
					'linkedin_url': existing_about.linkedin_url
				}
			else:
				aboutForm_existing = None
			aboutData_existing = aboutForm_existing
			aboutForm = profile_aboutmeForm(aboutForm_existing)

			#educationForm population and edit
			educationData = education.objects.filter(user_id = User_obj)
			if len(educationData) == 0:
				educationData = 'unavailable'
				educationInfoForm = None
			else:
				copy_educationData = educationData
				educationDataCounter = range(len(copy_educationData))
				educationData = zip(copy_educationData, educationDataCounter)
				educationEditForm = []
				for e in copy_educationData:
					e_dict = {
						'tuple_id': e.id,
						'year': e.year,
						'education_type': e.education_type,
						'institution': e.institution_name,
						'aggregate': e.aggregate,
						'what_did_you_do_there': e.what_did_you_do_there
					}
					el = profile_education_add_editForm(e_dict)
					educationEditForm.append(el)
				educationInfoForm = zip(educationEditForm, educationDataCounter)
			educationaddForm = profile_education_add_editForm()

			#workForm population and edit
			workData = work.objects.filter(user_id = User_obj)
			if len(workData) == 0:
				workData = 'unavailable'
				workInfoForm = None
			else:
				copy_workData = workData
				workDataCounter = range(len(copy_workData))
				workData = zip(copy_workData, workDataCounter)
				workEditForm = []
				for w in copy_workData:
					if w.work_type == 'Internship':
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'internship_company_name': w.internship_company_name,
							'internship_from_date': w.internship_date_from,
							'internship_to_date': w.internship_date_to,
							'internship_title': w.internship_title
						}
					elif w.work_type == 'Job':
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'job_company_name': w.job_company_name,
							'job_designation': w.job_designation,
							'job_from_date': w.job_date_from,
							'job_to_date': w.job_date_to
						}
					else:
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'freelancer_client': w.freelancer_client_name,
							'freelancer_project_title': w.freelancer_project_title,
							'freelancer_link': w.freelancer_link,
							'freelancer_project_status': w.freelancer_status,
							'freelancer_year': w.freelancer_year
						}
					wl = profile_work_add_editForm(w_dict)
					workEditForm.append(wl)
				workInfoForm = zip(workEditForm, workDataCounter)
			workaddForm = profile_work_add_editForm()

			#certificationForm populate and edit
			certificationData = certification.objects.filter(user_id = User_obj)
			if len(certificationData) == 0:
				certificationData = 'unavailable'
				certificationInfoForm = None
			else:
				copy_certificationData = certificationData
				certificationDataCounter = range(len(copy_certificationData))
				certificationData = zip(copy_certificationData, certificationDataCounter)
				certificationEditForm = []
				for c in copy_certificationData:
					c_dict = {
						'tuple_id': c.id,
						'year': c.year,
						'agency': c.agency,
						'mode': c.mode_of_certification,
						'details': c.details,					
					}		
					wl = profile_certification_add_editForm(c_dict)
					certificationEditForm.append(wl)
				certificationInfoForm = zip(certificationEditForm, certificationDataCounter)
			certificationaddForm = profile_certification_add_editForm()

			#extracurricularForm populate and edit
			exData = extracurricular_activities.objects.filter(user_id = User_obj)
			if len(exData) == 0:
				exData = 'unavailable'
				exInfoForm = None
			else:
				copy_exData = exData
				exDataCounter = range(len(copy_exData))
				exData = zip(copy_exData, exDataCounter)
				exEditForm = []
				for e in copy_exData:
					e_dict = {
						'tuple_id': e.id,
						'year': e.year,
						'activity_type': e.activity_type,
						'title': e.title,
						'details': e.activity_details,
						'organization': e.organization,
						'link': e.link					
					}			
					wl = profile_extracurricular_add_editForm(e_dict)
					exEditForm.append(wl)
				exInfoForm = zip(exEditForm, exDataCounter)
			extracurricularaddForm = profile_extracurricular_add_editForm()

			#achievementForm populate and edit
			achData = achievements.objects.filter(user_id = User_obj)
			if len(achData) == 0:
				achData = 'unavailable'
				achInfoForm = None
			else:
				copy_achData = achData
				achDataCounter = range(len(copy_achData))
				achData = zip(copy_achData, achDataCounter)
				achEditForm = []
				for a in copy_achData:
					a_dict = {
						'tuple_id': e.id,
						'year': a.year,
						'achievement_type': a.achievement_type,
						'title': a.title,
						'details': a.details,
						'organization': a.organization,
						'link': a.link					
					}			
					wl = profile_achievements_add_editForm(a_dict)
					achEditForm.append(wl)
				achInfoForm = zip(achEditForm, achDataCounter)
			achievementsaddForm = profile_achievements_add_editForm()

			#publicationForm populate and edit
			pubData = publication.objects.filter(user_id = User_obj)
			if len(pubData) == 0:
				pubData = 'unavailable'
				pubInfoForm = None
			else:
				copy_pubData = pubData
				pubDataCounter = range(len(copy_pubData))
				pubData = zip(copy_pubData, pubDataCounter)
				pubEditForm = []
				for p in copy_pubData:
					p_dict = {
						'tuple_id': p.id,
						'year': p.year,
						'mode': p.mode,
						'journal': p.journal,
						'status': p.status,				
						'details': p.details,					
						'link': p.link					
					}			
					wl = profile_publications_add_editForm(p_dict)
					pubEditForm.append(wl)
				pubInfoForm = zip(pubEditForm, pubDataCounter)
			publicationaddForm = profile_publications_add_editForm()

			#patentForm populate and edit
			patData = patent.objects.filter(user_id = User_obj)
			if len(patData) == 0:
				patData = 'unavailable'
				patInfoForm = None
			else:
				copy_patData = patData
				patDataCounter = range(len(copy_patData))
				patData = zip(copy_patData, patDataCounter)
				patEditForm = []
				for pa in copy_patData:
					pa_dict = {
						'tuple_id': pa.id,
						'year': pa.year,
						'mode': pa.mode,					
						'status': pa.patent_status,				
						'details': pa.patent_details
					}			
					wl = profile_patent_add_editForm(pa_dict)
					patEditForm.append(wl)
				patInfoForm = zip(patEditForm, patDataCounter)
			patentaddForm = profile_patent_add_editForm()

			skillsData = skills.objects.filter(user_id = User_obj)
			if len(skillsData) == 0:
				skillsData = 'unavailable'
				skillsInfoForm = None
			else:
				counter = 1
				skill_name_text = ''
				for s in skillsData:
					if counter == 1:
						skill_name_text = s.skill_name
					else:
						skill_name_text = skill_name_text + ',' + s.skill_name
					counter = counter + 1

				s_dict = {
					'skill': skill_name_text
				}
				skillsInfoForm = profile_skills_add_editForm(s_dict)
			skillsaddForm = profile_skills_add_editForm()

			variables = RequestContext(request, {
				'workForm': workForm,
				'educationForm': educationForm,
				'certificationForm': certificationForm,
				'publicationForm': publicationForm,
				'extracurricularForm': extracurricularForm,
				'patentForm': patentForm,
				'achievementForm': achievementForm,
				'aboutForm': aboutForm,
				'educationaddForm': educationaddForm,
				'workaddForm': workaddForm,
				'extracurricularaddForm': extracurricularaddForm,
				'certificationaddForm': certificationaddForm,
				'achievementsaddForm': achievementsaddForm,
				'publicationaddForm': publicationaddForm,
				'patentaddForm': patentaddForm,
				'aboutData': aboutData_existing,
				'educationData': educationData,	
				'educationInfoForm': educationInfoForm,
				'workData': workData,
				'workInfoForm': workInfoForm,
				'certificationData': certificationData,
				'certificationInfoForm': certificationInfoForm,
				'exData': exData,
				'exInfoForm': exInfoForm,
				'achData': achData,
				'achInfoForm': achInfoForm,
				'pubData': pubData,
				'pubInfoForm': pubInfoForm,
				'patData': patData,
				'patInfoForm': patInfoForm,
				'skillsaddForm': skillsaddForm,
				'skillsData': skillsData,
				'skillsInfoForm': skillsInfoForm,
				't_educationData': t_educationData,
				't_workData': t_workData,
				't_certificationData': t_certificationData,
				't_extracurricularData': t_extracurricularData,
				't_achievementData': t_achievementData,
				't_publicationData': t_publicationData,
				't_patentData': t_patentData
			})
			return render_to_response('profile-page.html', variables)

	elif request.method=='GET' and 'extracurriculareditForm' in request.GET:
		extracurricularaddForm = profile_extracurricular_add_editForm(request.GET)
		if extracurricularaddForm.is_valid():
			row_id = extracurricularaddForm.cleaned_data['tuple_id']
			year = extracurricularaddForm.cleaned_data['year']
			activity_type = extracurricularaddForm.cleaned_data['activity_type']
			title = extracurricularaddForm.cleaned_data['title']
			details = extracurricularaddForm.cleaned_data['details']
			organization = extracurricularaddForm.cleaned_data['organization']
			link = extracurricularaddForm.cleaned_data['link']

			extracurricular_obj = extracurricular_activities.objects.get(id = row_id)

			extracurricular_obj.year = year
			extracurricular_obj.activity_type = activity_type
			extracurricular_obj.title = title
			extracurricular_obj.activity_details = details
			extracurricular_obj.organization = organization
			extracurricular_obj.link = link

			extracurricular_obj.save()
			status = {
				'error': False,
				'error_message': '',
				'success': True,
				'success_message': 'Extracurricular details saved.',
			}
			workForm = profile_workForm()
			educationForm = profile_educationForm()
			certificationForm = profile_certificationForm()
			publicationForm = profile_publicationForm()
			extracurricularForm = profile_extracurricularForm()
			patentForm = profile_patentForm()
			achievementForm = profile_achievementForm()
			t_educationData = education.objects.filter(user_id = User_obj)
			if len(t_educationData) == 0:
				t_educationData = 'unavailable'
			else:
				t_educationData = zip(t_educationData, range(len(t_educationData)))
			t_workData = work.objects.filter(user_id = User_obj)
			if len(t_workData) == 0:
				t_workData = 'unavailable'
			else:
				t_workData = zip(t_workData, range(len(t_workData)))
			t_certificationData = certification.objects.filter(user_id = User_obj)
			if len(t_certificationData) == 0:
				t_certificationData = 'unavailable'
			else:
				t_certificationData = zip(t_certificationData, range(len(t_certificationData)))
			t_extracurricularData = extracurricular_activities.objects.filter(user_id = User_obj)
			if len(t_extracurricularData) == 0:
				t_extracurricularData = 'unavailable'
			else:
				t_extracurricularData = zip(t_extracurricularData, range(len(t_extracurricularData)))
			t_achievementData = achievements.objects.filter(user_id = User_obj)
			if len(t_achievementData) == 0:
				t_achievementData = 'unavailable'
			else:
				t_achievementData = zip(t_achievementData, range(len(t_achievementData)))
			t_publicationData = publication.objects.filter(user_id = User_obj)
			if len(t_publicationData) == 0:
				t_publicationData = 'unavailable'
			else:
				t_publicationData = zip(t_publicationData, range(len(t_publicationData)))
			t_patentData = patent.objects.filter(user_id = User_obj)					
			if len(t_patentData) == 0:
				t_patentData = 'unavailable'
			else:
				t_patentData = zip(t_patentData, range(len(t_patentData)))


			
			# aboutForm population
			try:
				existing_about = user_details.objects.get(user_id = User_obj)
			except:
				existing_about = 'unavailable'
			if existing_about!='unavailable':
				aboutForm_existing = {
					'profession': existing_about.profession,
					'first_name': existing_about.first_name,
					'last_name': existing_about.last_name,
					'dob': existing_about.dob,
					'short_bio': existing_about.short_bio,
					'facebook_url': existing_about.facebook_url,
					'twitter_handle': existing_about.twitter_handle,
					'linkedin_url': existing_about.linkedin_url
				}
			else:
				aboutForm_existing = None
			aboutData_existing = aboutForm_existing
			aboutForm = profile_aboutmeForm(aboutForm_existing)

			#educationForm population and edit
			educationData = education.objects.filter(user_id = User_obj)
			if len(educationData) == 0:
				educationData = 'unavailable'
				educationInfoForm = None
			else:
				copy_educationData = educationData
				educationDataCounter = range(len(copy_educationData))
				educationData = zip(copy_educationData, educationDataCounter)
				educationEditForm = []
				for e in copy_educationData:
					e_dict = {
						'tuple_id': e.id,
						'year': e.year,
						'education_type': e.education_type,
						'institution': e.institution_name,
						'aggregate': e.aggregate,
						'what_did_you_do_there': e.what_did_you_do_there
					}
					el = profile_education_add_editForm(e_dict)
					educationEditForm.append(el)
				educationInfoForm = zip(educationEditForm, educationDataCounter)
			educationaddForm = profile_education_add_editForm()

			#workForm population and edit
			workData = work.objects.filter(user_id = User_obj)
			if len(workData) == 0:
				workData = 'unavailable'
				workInfoForm = None
			else:
				copy_workData = workData
				workDataCounter = range(len(copy_workData))
				workData = zip(copy_workData, workDataCounter)
				workEditForm = []
				for w in copy_workData:
					if w.work_type == 'Internship':
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'internship_company_name': w.internship_company_name,
							'internship_from_date': w.internship_date_from,
							'internship_to_date': w.internship_date_to,
							'internship_title': w.internship_title
						}
					elif w.work_type == 'Job':
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'job_company_name': w.job_company_name,
							'job_designation': w.job_designation,
							'job_from_date': w.job_date_from,
							'job_to_date': w.job_date_to
						}
					else:
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'freelancer_client': w.freelancer_client_name,
							'freelancer_project_title': w.freelancer_project_title,
							'freelancer_link': w.freelancer_link,
							'freelancer_project_status': w.freelancer_status,
							'freelancer_year': w.freelancer_year
						}
					wl = profile_work_add_editForm(w_dict)
					workEditForm.append(wl)
				workInfoForm = zip(workEditForm, workDataCounter)
			workaddForm = profile_work_add_editForm()

			#certificationForm populate and edit
			certificationData = certification.objects.filter(user_id = User_obj)
			if len(certificationData) == 0:
				certificationData = 'unavailable'
				certificationInfoForm = None
			else:
				copy_certificationData = certificationData
				certificationDataCounter = range(len(copy_certificationData))
				certificationData = zip(copy_certificationData, certificationDataCounter)
				certificationEditForm = []
				for c in copy_certificationData:
					c_dict = {
						'tuple_id': c.id,
						'year': c.year,
						'agency': c.agency,
						'mode': c.mode_of_certification,
						'details': c.details,					
					}		
					wl = profile_certification_add_editForm(c_dict)
					certificationEditForm.append(wl)
				certificationInfoForm = zip(certificationEditForm, certificationDataCounter)
			certificationaddForm = profile_certification_add_editForm()

			#extracurricularForm populate and edit
			exData = extracurricular_activities.objects.filter(user_id = User_obj)
			if len(exData) == 0:
				exData = 'unavailable'
				exInfoForm = None
			else:
				copy_exData = exData
				exDataCounter = range(len(copy_exData))
				exData = zip(copy_exData, exDataCounter)
				exEditForm = []
				for e in copy_exData:
					e_dict = {
						'tuple_id': e.id,
						'year': e.year,
						'activity_type': e.activity_type,
						'title': e.title,
						'details': e.activity_details,
						'organization': e.organization,
						'link': e.link					
					}			
					wl = profile_extracurricular_add_editForm(e_dict)
					exEditForm.append(wl)
				exInfoForm = zip(exEditForm, exDataCounter)
			extracurricularaddForm = profile_extracurricular_add_editForm()

			#achievementForm populate and edit
			achData = achievements.objects.filter(user_id = User_obj)
			if len(achData) == 0:
				achData = 'unavailable'
				achInfoForm = None
			else:
				copy_achData = achData
				achDataCounter = range(len(copy_achData))
				achData = zip(copy_achData, achDataCounter)
				achEditForm = []
				for a in copy_achData:
					a_dict = {
						'tuple_id': e.id,
						'year': a.year,
						'achievement_type': a.achievement_type,
						'title': a.title,
						'details': a.details,
						'organization': a.organization,
						'link': a.link					
					}			
					wl = profile_achievements_add_editForm(a_dict)
					achEditForm.append(wl)
				achInfoForm = zip(achEditForm, achDataCounter)
			achievementsaddForm = profile_achievements_add_editForm()

			#publicationForm populate and edit
			pubData = publication.objects.filter(user_id = User_obj)
			if len(pubData) == 0:
				pubData = 'unavailable'
				pubInfoForm = None
			else:
				copy_pubData = pubData
				pubDataCounter = range(len(copy_pubData))
				pubData = zip(copy_pubData, pubDataCounter)
				pubEditForm = []
				for p in copy_pubData:
					p_dict = {
						'tuple_id': p.id,
						'year': p.year,
						'mode': p.mode,
						'journal': p.journal,
						'status': p.status,				
						'details': p.details,					
						'link': p.link					
					}			
					wl = profile_publications_add_editForm(p_dict)
					pubEditForm.append(wl)
				pubInfoForm = zip(pubEditForm, pubDataCounter)
			publicationaddForm = profile_publications_add_editForm()

			#patentForm populate and edit
			patData = patent.objects.filter(user_id = User_obj)
			if len(patData) == 0:
				patData = 'unavailable'
				patInfoForm = None
			else:
				copy_patData = patData
				patDataCounter = range(len(copy_patData))
				patData = zip(copy_patData, patDataCounter)
				patEditForm = []
				for pa in copy_patData:
					pa_dict = {
						'tuple_id': pa.id,
						'year': pa.year,
						'mode': pa.mode,					
						'status': pa.patent_status,				
						'details': pa.patent_details
					}			
					wl = profile_patent_add_editForm(pa_dict)
					patEditForm.append(wl)
				patInfoForm = zip(patEditForm, patDataCounter)
			patentaddForm = profile_patent_add_editForm()

			skillsData = skills.objects.filter(user_id = User_obj)
			if len(skillsData) == 0:
				skillsData = 'unavailable'
				skillsInfoForm = None
			else:
				counter = 1
				skill_name_text = ''
				for s in skillsData:
					if counter == 1:
						skill_name_text = s.skill_name
					else:
						skill_name_text = skill_name_text + ',' + s.skill_name
					counter = counter + 1

				s_dict = {
					'skill': skill_name_text
				}
				skillsInfoForm = profile_skills_add_editForm(s_dict)
			skillsaddForm = profile_skills_add_editForm()

			variables = RequestContext(request, {
				'workForm': workForm,
				'educationForm': educationForm,
				'certificationForm': certificationForm,
				'publicationForm': publicationForm,
				'extracurricularForm': extracurricularForm,
				'patentForm': patentForm,
				'achievementForm': achievementForm,
				'aboutForm': aboutForm,
				'educationaddForm': educationaddForm,
				'workaddForm': workaddForm,
				'extracurricularaddForm': extracurricularaddForm,
				'certificationaddForm': certificationaddForm,
				'achievementsaddForm': achievementsaddForm,
				'publicationaddForm': publicationaddForm,
				'patentaddForm': patentaddForm,
				'aboutData': aboutData_existing,
				'educationData': educationData,	
				'educationInfoForm': educationInfoForm,
				'workData': workData,
				'workInfoForm': workInfoForm,
				'certificationData': certificationData,
				'certificationInfoForm': certificationInfoForm,
				'exData': exData,
				'exInfoForm': exInfoForm,
				'achData': achData,
				'achInfoForm': achInfoForm,
				'pubData': pubData,
				'pubInfoForm': pubInfoForm,
				'patData': patData,
				'patInfoForm': patInfoForm,
				'skillsaddForm': skillsaddForm,
				'skillsData': skillsData,
				'skillsInfoForm': skillsInfoForm,
				't_educationData': t_educationData,
				't_workData': t_workData,
				't_certificationData': t_certificationData,
				't_extracurricularData': t_extracurricularData,
				't_achievementData': t_achievementData,
				't_publicationData': t_publicationData,
				't_patentData': t_patentData
			})
			return render_to_response('profile-page.html', variables)

	elif request.method=='GET' and 'extracurriculardeleteForm' in request.GET:
		extracurricularaddForm = profile_extracurricular_add_editForm(request.GET)
		if extracurricularaddForm.is_valid():
			row_id = extracurricularaddForm.cleaned_data['tuple_id']
			# year = extracurricularaddForm.cleaned_data['year']
			# activity_type = extracurricularaddForm.cleaned_data['activity_type']
			# title = extracurricularaddForm.cleaned_data['title']
			# details = extracurricularaddForm.cleaned_data['details']
			# organization = extracurricularaddForm.cleaned_data['organization']
			# link = extracurricularaddForm.cleaned_data['link']

			extracurricular_obj = extracurricular_activities.objects.get(id = row_id)

			extracurricular_obj.delete()
			status = {
				'error': False,
				'error_message': '',
				'success': True,
				'success_message': 'Extracurricular details deleted.',
			}
			workForm = profile_workForm()
			educationForm = profile_educationForm()
			certificationForm = profile_certificationForm()
			publicationForm = profile_publicationForm()
			extracurricularForm = profile_extracurricularForm()
			patentForm = profile_patentForm()
			achievementForm = profile_achievementForm()
			t_educationData = education.objects.filter(user_id = User_obj)
			if len(t_educationData) == 0:
				t_educationData = 'unavailable'
			else:
				t_educationData = zip(t_educationData, range(len(t_educationData)))
			t_workData = work.objects.filter(user_id = User_obj)
			if len(t_workData) == 0:
				t_workData = 'unavailable'
			else:
				t_workData = zip(t_workData, range(len(t_workData)))
			t_certificationData = certification.objects.filter(user_id = User_obj)
			if len(t_certificationData) == 0:
				t_certificationData = 'unavailable'
			else:
				t_certificationData = zip(t_certificationData, range(len(t_certificationData)))
			t_extracurricularData = extracurricular_activities.objects.filter(user_id = User_obj)
			if len(t_extracurricularData) == 0:
				t_extracurricularData = 'unavailable'
			else:
				t_extracurricularData = zip(t_extracurricularData, range(len(t_extracurricularData)))
			t_achievementData = achievements.objects.filter(user_id = User_obj)
			if len(t_achievementData) == 0:
				t_achievementData = 'unavailable'
			else:
				t_achievementData = zip(t_achievementData, range(len(t_achievementData)))
			t_publicationData = publication.objects.filter(user_id = User_obj)
			if len(t_publicationData) == 0:
				t_publicationData = 'unavailable'
			else:
				t_publicationData = zip(t_publicationData, range(len(t_publicationData)))
			t_patentData = patent.objects.filter(user_id = User_obj)					
			if len(t_patentData) == 0:
				t_patentData = 'unavailable'
			else:
				t_patentData = zip(t_patentData, range(len(t_patentData)))


			
			# aboutForm population
			try:
				existing_about = user_details.objects.get(user_id = User_obj)
			except:
				existing_about = 'unavailable'
			if existing_about!='unavailable':
				aboutForm_existing = {
					'profession': existing_about.profession,
					'first_name': existing_about.first_name,
					'last_name': existing_about.last_name,
					'dob': existing_about.dob,
					'short_bio': existing_about.short_bio,
					'facebook_url': existing_about.facebook_url,
					'twitter_handle': existing_about.twitter_handle,
					'linkedin_url': existing_about.linkedin_url
				}
			else:
				aboutForm_existing = None
			aboutData_existing = aboutForm_existing
			aboutForm = profile_aboutmeForm(aboutForm_existing)

			#educationForm population and edit
			educationData = education.objects.filter(user_id = User_obj)
			if len(educationData) == 0:
				educationData = 'unavailable'
				educationInfoForm = None
			else:
				copy_educationData = educationData
				educationDataCounter = range(len(copy_educationData))
				educationData = zip(copy_educationData, educationDataCounter)
				educationEditForm = []
				for e in copy_educationData:
					e_dict = {
						'tuple_id': e.id,
						'year': e.year,
						'education_type': e.education_type,
						'institution': e.institution_name,
						'aggregate': e.aggregate,
						'what_did_you_do_there': e.what_did_you_do_there
					}
					el = profile_education_add_editForm(e_dict)
					educationEditForm.append(el)
				educationInfoForm = zip(educationEditForm, educationDataCounter)
			educationaddForm = profile_education_add_editForm()

			#workForm population and edit
			workData = work.objects.filter(user_id = User_obj)
			if len(workData) == 0:
				workData = 'unavailable'
				workInfoForm = None
			else:
				copy_workData = workData
				workDataCounter = range(len(copy_workData))
				workData = zip(copy_workData, workDataCounter)
				workEditForm = []
				for w in copy_workData:
					if w.work_type == 'Internship':
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'internship_company_name': w.internship_company_name,
							'internship_from_date': w.internship_date_from,
							'internship_to_date': w.internship_date_to,
							'internship_title': w.internship_title
						}
					elif w.work_type == 'Job':
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'job_company_name': w.job_company_name,
							'job_designation': w.job_designation,
							'job_from_date': w.job_date_from,
							'job_to_date': w.job_date_to
						}
					else:
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'freelancer_client': w.freelancer_client_name,
							'freelancer_project_title': w.freelancer_project_title,
							'freelancer_link': w.freelancer_link,
							'freelancer_project_status': w.freelancer_status,
							'freelancer_year': w.freelancer_year
						}
					wl = profile_work_add_editForm(w_dict)
					workEditForm.append(wl)
				workInfoForm = zip(workEditForm, workDataCounter)
			workaddForm = profile_work_add_editForm()

			#certificationForm populate and edit
			certificationData = certification.objects.filter(user_id = User_obj)
			if len(certificationData) == 0:
				certificationData = 'unavailable'
				certificationInfoForm = None
			else:
				copy_certificationData = certificationData
				certificationDataCounter = range(len(copy_certificationData))
				certificationData = zip(copy_certificationData, certificationDataCounter)
				certificationEditForm = []
				for c in copy_certificationData:
					c_dict = {
						'tuple_id': c.id,
						'year': c.year,
						'agency': c.agency,
						'mode': c.mode_of_certification,
						'details': c.details,					
					}		
					wl = profile_certification_add_editForm(c_dict)
					certificationEditForm.append(wl)
				certificationInfoForm = zip(certificationEditForm, certificationDataCounter)
			certificationaddForm = profile_certification_add_editForm()

			#extracurricularForm populate and edit
			exData = extracurricular_activities.objects.filter(user_id = User_obj)
			if len(exData) == 0:
				exData = 'unavailable'
				exInfoForm = None
			else:
				copy_exData = exData
				exDataCounter = range(len(copy_exData))
				exData = zip(copy_exData, exDataCounter)
				exEditForm = []
				for e in copy_exData:
					e_dict = {
						'tuple_id': e.id,
						'year': e.year,
						'activity_type': e.activity_type,
						'title': e.title,
						'details': e.activity_details,
						'organization': e.organization,
						'link': e.link					
					}			
					wl = profile_extracurricular_add_editForm(e_dict)
					exEditForm.append(wl)
				exInfoForm = zip(exEditForm, exDataCounter)
			extracurricularaddForm = profile_extracurricular_add_editForm()

			#achievementForm populate and edit
			achData = achievements.objects.filter(user_id = User_obj)
			if len(achData) == 0:
				achData = 'unavailable'
				achInfoForm = None
			else:
				copy_achData = achData
				achDataCounter = range(len(copy_achData))
				achData = zip(copy_achData, achDataCounter)
				achEditForm = []
				for a in copy_achData:
					a_dict = {
						'tuple_id': e.id,
						'year': a.year,
						'achievement_type': a.achievement_type,
						'title': a.title,
						'details': a.details,
						'organization': a.organization,
						'link': a.link					
					}			
					wl = profile_achievements_add_editForm(a_dict)
					achEditForm.append(wl)
				achInfoForm = zip(achEditForm, achDataCounter)
			achievementsaddForm = profile_achievements_add_editForm()

			#publicationForm populate and edit
			pubData = publication.objects.filter(user_id = User_obj)
			if len(pubData) == 0:
				pubData = 'unavailable'
				pubInfoForm = None
			else:
				copy_pubData = pubData
				pubDataCounter = range(len(copy_pubData))
				pubData = zip(copy_pubData, pubDataCounter)
				pubEditForm = []
				for p in copy_pubData:
					p_dict = {
						'tuple_id': p.id,
						'year': p.year,
						'mode': p.mode,
						'journal': p.journal,
						'status': p.status,				
						'details': p.details,					
						'link': p.link					
					}			
					wl = profile_publications_add_editForm(p_dict)
					pubEditForm.append(wl)
				pubInfoForm = zip(pubEditForm, pubDataCounter)
			publicationaddForm = profile_publications_add_editForm()

			#patentForm populate and edit
			patData = patent.objects.filter(user_id = User_obj)
			if len(patData) == 0:
				patData = 'unavailable'
				patInfoForm = None
			else:
				copy_patData = patData
				patDataCounter = range(len(copy_patData))
				patData = zip(copy_patData, patDataCounter)
				patEditForm = []
				for pa in copy_patData:
					pa_dict = {
						'tuple_id': pa.id,
						'year': pa.year,
						'mode': pa.mode,					
						'status': pa.patent_status,				
						'details': pa.patent_details
					}			
					wl = profile_patent_add_editForm(pa_dict)
					patEditForm.append(wl)
				patInfoForm = zip(patEditForm, patDataCounter)
			patentaddForm = profile_patent_add_editForm()

			skillsData = skills.objects.filter(user_id = User_obj)
			if len(skillsData) == 0:
				skillsData = 'unavailable'
				skillsInfoForm = None
			else:
				counter = 1
				skill_name_text = ''
				for s in skillsData:
					if counter == 1:
						skill_name_text = s.skill_name
					else:
						skill_name_text = skill_name_text + ',' + s.skill_name
					counter = counter + 1

				s_dict = {
					'skill': skill_name_text
				}
				skillsInfoForm = profile_skills_add_editForm(s_dict)
			skillsaddForm = profile_skills_add_editForm()

			variables = RequestContext(request, {
				'workForm': workForm,
				'educationForm': educationForm,
				'certificationForm': certificationForm,
				'publicationForm': publicationForm,
				'extracurricularForm': extracurricularForm,
				'patentForm': patentForm,
				'achievementForm': achievementForm,
				'aboutForm': aboutForm,
				'educationaddForm': educationaddForm,
				'workaddForm': workaddForm,
				'extracurricularaddForm': extracurricularaddForm,
				'certificationaddForm': certificationaddForm,
				'achievementsaddForm': achievementsaddForm,
				'publicationaddForm': publicationaddForm,
				'patentaddForm': patentaddForm,
				'aboutData': aboutData_existing,
				'educationData': educationData,	
				'educationInfoForm': educationInfoForm,
				'workData': workData,
				'workInfoForm': workInfoForm,
				'certificationData': certificationData,
				'certificationInfoForm': certificationInfoForm,
				'exData': exData,
				'exInfoForm': exInfoForm,
				'achData': achData,
				'achInfoForm': achInfoForm,
				'pubData': pubData,
				'pubInfoForm': pubInfoForm,
				'patData': patData,
				'patInfoForm': patInfoForm,
				'skillsaddForm': skillsaddForm,
				'skillsData': skillsData,
				'skillsInfoForm': skillsInfoForm,
				't_educationData': t_educationData,
				't_workData': t_workData,
				't_certificationData': t_certificationData,
				't_extracurricularData': t_extracurricularData,
				't_achievementData': t_achievementData,
				't_publicationData': t_publicationData,
				't_patentData': t_patentData
			})
			return render_to_response('profile-page.html', variables)

	elif request.method=='GET' and 'patentaddForm' in request.GET:
		patentaddForm = profile_patent_add_editForm(request.GET)
		if patentaddForm.is_valid():
			year = patentaddForm.cleaned_data['year']
			mode = patentaddForm.cleaned_data['mode']
			status = patentaddForm.cleaned_data['status']
			details = patentaddForm.cleaned_data['details']

			patent_obj = patent(
				user_id = User_obj,
				year = year,
				mode = mode,
				patent_details = details,
				patent_status = status
			)
			patent_obj.save()
			status = {
				'error': False,
				'error_message': '',
				'success': True,
				'success_message': 'Patent details saved.',
			}
			workForm = profile_workForm()
			educationForm = profile_educationForm()
			certificationForm = profile_certificationForm()
			publicationForm = profile_publicationForm()
			extracurricularForm = profile_extracurricularForm()
			patentForm = profile_patentForm()
			achievementForm = profile_achievementForm()
			t_educationData = education.objects.filter(user_id = User_obj)
			if len(t_educationData) == 0:
				t_educationData = 'unavailable'
			else:
				t_educationData = zip(t_educationData, range(len(t_educationData)))
			t_workData = work.objects.filter(user_id = User_obj)
			if len(t_workData) == 0:
				t_workData = 'unavailable'
			else:
				t_workData = zip(t_workData, range(len(t_workData)))
			t_certificationData = certification.objects.filter(user_id = User_obj)
			if len(t_certificationData) == 0:
				t_certificationData = 'unavailable'
			else:
				t_certificationData = zip(t_certificationData, range(len(t_certificationData)))
			t_extracurricularData = extracurricular_activities.objects.filter(user_id = User_obj)
			if len(t_extracurricularData) == 0:
				t_extracurricularData = 'unavailable'
			else:
				t_extracurricularData = zip(t_extracurricularData, range(len(t_extracurricularData)))
			t_achievementData = achievements.objects.filter(user_id = User_obj)
			if len(t_achievementData) == 0:
				t_achievementData = 'unavailable'
			else:
				t_achievementData = zip(t_achievementData, range(len(t_achievementData)))
			t_publicationData = publication.objects.filter(user_id = User_obj)
			if len(t_publicationData) == 0:
				t_publicationData = 'unavailable'
			else:
				t_publicationData = zip(t_publicationData, range(len(t_publicationData)))
			t_patentData = patent.objects.filter(user_id = User_obj)					
			if len(t_patentData) == 0:
				t_patentData = 'unavailable'
			else:
				t_patentData = zip(t_patentData, range(len(t_patentData)))


			
			# aboutForm population
			try:
				existing_about = user_details.objects.get(user_id = User_obj)
			except:
				existing_about = 'unavailable'
			if existing_about!='unavailable':
				aboutForm_existing = {
					'profession': existing_about.profession,
					'first_name': existing_about.first_name,
					'last_name': existing_about.last_name,
					'dob': existing_about.dob,
					'short_bio': existing_about.short_bio,
					'facebook_url': existing_about.facebook_url,
					'twitter_handle': existing_about.twitter_handle,
					'linkedin_url': existing_about.linkedin_url
				}
			else:
				aboutForm_existing = None
			aboutData_existing = aboutForm_existing
			aboutForm = profile_aboutmeForm(aboutForm_existing)

			#educationForm population and edit
			educationData = education.objects.filter(user_id = User_obj)
			if len(educationData) == 0:
				educationData = 'unavailable'
				educationInfoForm = None
			else:
				copy_educationData = educationData
				educationDataCounter = range(len(copy_educationData))
				educationData = zip(copy_educationData, educationDataCounter)
				educationEditForm = []
				for e in copy_educationData:
					e_dict = {
						'tuple_id': e.id,
						'year': e.year,
						'education_type': e.education_type,
						'institution': e.institution_name,
						'aggregate': e.aggregate,
						'what_did_you_do_there': e.what_did_you_do_there
					}
					el = profile_education_add_editForm(e_dict)
					educationEditForm.append(el)
				educationInfoForm = zip(educationEditForm, educationDataCounter)
			educationaddForm = profile_education_add_editForm()

			#workForm population and edit
			workData = work.objects.filter(user_id = User_obj)
			if len(workData) == 0:
				workData = 'unavailable'
				workInfoForm = None
			else:
				copy_workData = workData
				workDataCounter = range(len(copy_workData))
				workData = zip(copy_workData, workDataCounter)
				workEditForm = []
				for w in copy_workData:
					if w.work_type == 'Internship':
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'internship_company_name': w.internship_company_name,
							'internship_from_date': w.internship_date_from,
							'internship_to_date': w.internship_date_to,
							'internship_title': w.internship_title
						}
					elif w.work_type == 'Job':
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'job_company_name': w.job_company_name,
							'job_designation': w.job_designation,
							'job_from_date': w.job_date_from,
							'job_to_date': w.job_date_to
						}
					else:
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'freelancer_client': w.freelancer_client_name,
							'freelancer_project_title': w.freelancer_project_title,
							'freelancer_link': w.freelancer_link,
							'freelancer_project_status': w.freelancer_status,
							'freelancer_year': w.freelancer_year
						}
					wl = profile_work_add_editForm(w_dict)
					workEditForm.append(wl)
				workInfoForm = zip(workEditForm, workDataCounter)
			workaddForm = profile_work_add_editForm()

			#certificationForm populate and edit
			certificationData = certification.objects.filter(user_id = User_obj)
			if len(certificationData) == 0:
				certificationData = 'unavailable'
				certificationInfoForm = None
			else:
				copy_certificationData = certificationData
				certificationDataCounter = range(len(copy_certificationData))
				certificationData = zip(copy_certificationData, certificationDataCounter)
				certificationEditForm = []
				for c in copy_certificationData:
					c_dict = {
						'tuple_id': c.id,
						'year': c.year,
						'agency': c.agency,
						'mode': c.mode_of_certification,
						'details': c.details,					
					}		
					wl = profile_certification_add_editForm(c_dict)
					certificationEditForm.append(wl)
				certificationInfoForm = zip(certificationEditForm, certificationDataCounter)
			certificationaddForm = profile_certification_add_editForm()

			#extracurricularForm populate and edit
			exData = extracurricular_activities.objects.filter(user_id = User_obj)
			if len(exData) == 0:
				exData = 'unavailable'
				exInfoForm = None
			else:
				copy_exData = exData
				exDataCounter = range(len(copy_exData))
				exData = zip(copy_exData, exDataCounter)
				exEditForm = []
				for e in copy_exData:
					e_dict = {
						'tuple_id': e.id,
						'year': e.year,
						'activity_type': e.activity_type,
						'title': e.title,
						'details': e.activity_details,
						'organization': e.organization,
						'link': e.link					
					}			
					wl = profile_extracurricular_add_editForm(e_dict)
					exEditForm.append(wl)
				exInfoForm = zip(exEditForm, exDataCounter)
			extracurricularaddForm = profile_extracurricular_add_editForm()

			#achievementForm populate and edit
			achData = achievements.objects.filter(user_id = User_obj)
			if len(achData) == 0:
				achData = 'unavailable'
				achInfoForm = None
			else:
				copy_achData = achData
				achDataCounter = range(len(copy_achData))
				achData = zip(copy_achData, achDataCounter)
				achEditForm = []
				for a in copy_achData:
					a_dict = {
						'tuple_id': a.id,
						'year': a.year,
						'achievement_type': a.achievement_type,
						'title': a.title,
						'details': a.details,
						'organization': a.organization,
						'link': a.link					
					}			
					wl = profile_achievements_add_editForm(a_dict)
					achEditForm.append(wl)
				achInfoForm = zip(achEditForm, achDataCounter)
			achievementsaddForm = profile_achievements_add_editForm()

			#publicationForm populate and edit
			pubData = publication.objects.filter(user_id = User_obj)
			if len(pubData) == 0:
				pubData = 'unavailable'
				pubInfoForm = None
			else:
				copy_pubData = pubData
				pubDataCounter = range(len(copy_pubData))
				pubData = zip(copy_pubData, pubDataCounter)
				pubEditForm = []
				for p in copy_pubData:
					p_dict = {
						'tuple_id': p.id,
						'year': p.year,
						'mode': p.mode,
						'journal': p.journal,
						'status': p.status,				
						'details': p.details,					
						'link': p.link					
					}			
					wl = profile_publications_add_editForm(p_dict)
					pubEditForm.append(wl)
				pubInfoForm = zip(pubEditForm, pubDataCounter)
			publicationaddForm = profile_publications_add_editForm()

			#patentForm populate and edit
			patData = patent.objects.filter(user_id = User_obj)
			if len(patData) == 0:
				patData = 'unavailable'
				patInfoForm = None
			else:
				copy_patData = patData
				patDataCounter = range(len(copy_patData))
				patData = zip(copy_patData, patDataCounter)
				patEditForm = []
				for pa in copy_patData:
					pa_dict = {
						'tuple_id': pa.id,
						'year': pa.year,
						'mode': pa.mode,					
						'status': pa.patent_status,				
						'details': pa.patent_details
					}			
					wl = profile_patent_add_editForm(pa_dict)
					patEditForm.append(wl)
				patInfoForm = zip(patEditForm, patDataCounter)
			patentaddForm = profile_patent_add_editForm()

			skillsData = skills.objects.filter(user_id = User_obj)
			if len(skillsData) == 0:
				skillsData = 'unavailable'
				skillsInfoForm = None
			else:
				counter = 1
				skill_name_text = ''
				for s in skillsData:
					if counter == 1:
						skill_name_text = s.skill_name
					else:
						skill_name_text = skill_name_text + ',' + s.skill_name
					counter = counter + 1

				s_dict = {
					'skill': skill_name_text
				}
				skillsInfoForm = profile_skills_add_editForm(s_dict)
			skillsaddForm = profile_skills_add_editForm()

			variables = RequestContext(request, {
				'workForm': workForm,
				'educationForm': educationForm,
				'certificationForm': certificationForm,
				'publicationForm': publicationForm,
				'extracurricularForm': extracurricularForm,
				'patentForm': patentForm,
				'achievementForm': achievementForm,
				'aboutForm': aboutForm,
				'educationaddForm': educationaddForm,
				'workaddForm': workaddForm,
				'extracurricularaddForm': extracurricularaddForm,
				'certificationaddForm': certificationaddForm,
				'achievementsaddForm': achievementsaddForm,
				'publicationaddForm': publicationaddForm,
				'patentaddForm': patentaddForm,
				'aboutData': aboutData_existing,
				'educationData': educationData,	
				'educationInfoForm': educationInfoForm,
				'workData': workData,
				'workInfoForm': workInfoForm,
				'certificationData': certificationData,
				'certificationInfoForm': certificationInfoForm,
				'exData': exData,
				'exInfoForm': exInfoForm,
				'achData': achData,
				'achInfoForm': achInfoForm,
				'pubData': pubData,
				'pubInfoForm': pubInfoForm,
				'patData': patData,
				'patInfoForm': patInfoForm,
				'skillsaddForm': skillsaddForm,
				'skillsData': skillsData,
				'skillsInfoForm': skillsInfoForm,
				't_educationData': t_educationData,
				't_workData': t_workData,
				't_certificationData': t_certificationData,
				't_extracurricularData': t_extracurricularData,
				't_achievementData': t_achievementData,
				't_publicationData': t_publicationData,
				't_patentData': t_patentData
			})
			return render_to_response('profile-page.html', variables)

	elif request.method=='GET' and 'patentdeleteForm' in request.GET:
		patentaddForm = profile_patent_add_editForm(request.GET)
		if patentaddForm.is_valid():
			row_id = patentaddForm.cleaned_data['tuple_id']			

			patent_obj = patent.objects.get(id = row_id)

			patent_obj.delete()
			status = {
				'error': False,
				'error_message': '',
				'success': True,
				'success_message': 'Patent details deleted.',
			}
			workForm = profile_workForm()
			educationForm = profile_educationForm()
			certificationForm = profile_certificationForm()
			publicationForm = profile_publicationForm()
			extracurricularForm = profile_extracurricularForm()
			patentForm = profile_patentForm()
			achievementForm = profile_achievementForm()
			t_educationData = education.objects.filter(user_id = User_obj)
			if len(t_educationData) == 0:
				t_educationData = 'unavailable'
			else:
				t_educationData = zip(t_educationData, range(len(t_educationData)))
			t_workData = work.objects.filter(user_id = User_obj)
			if len(t_workData) == 0:
				t_workData = 'unavailable'
			else:
				t_workData = zip(t_workData, range(len(t_workData)))
			t_certificationData = certification.objects.filter(user_id = User_obj)
			if len(t_certificationData) == 0:
				t_certificationData = 'unavailable'
			else:
				t_certificationData = zip(t_certificationData, range(len(t_certificationData)))
			t_extracurricularData = extracurricular_activities.objects.filter(user_id = User_obj)
			if len(t_extracurricularData) == 0:
				t_extracurricularData = 'unavailable'
			else:
				t_extracurricularData = zip(t_extracurricularData, range(len(t_extracurricularData)))
			t_achievementData = achievements.objects.filter(user_id = User_obj)
			if len(t_achievementData) == 0:
				t_achievementData = 'unavailable'
			else:
				t_achievementData = zip(t_achievementData, range(len(t_achievementData)))
			t_publicationData = publication.objects.filter(user_id = User_obj)
			if len(t_publicationData) == 0:
				t_publicationData = 'unavailable'
			else:
				t_publicationData = zip(t_publicationData, range(len(t_publicationData)))
			t_patentData = patent.objects.filter(user_id = User_obj)					
			if len(t_patentData) == 0:
				t_patentData = 'unavailable'
			else:
				t_patentData = zip(t_patentData, range(len(t_patentData)))


			
			# aboutForm population
			try:
				existing_about = user_details.objects.get(user_id = User_obj)
			except:
				existing_about = 'unavailable'
			if existing_about!='unavailable':
				aboutForm_existing = {
					'profession': existing_about.profession,
					'first_name': existing_about.first_name,
					'last_name': existing_about.last_name,
					'dob': existing_about.dob,
					'short_bio': existing_about.short_bio,
					'facebook_url': existing_about.facebook_url,
					'twitter_handle': existing_about.twitter_handle,
					'linkedin_url': existing_about.linkedin_url
				}
			else:
				aboutForm_existing = None
			aboutData_existing = aboutForm_existing
			aboutForm = profile_aboutmeForm(aboutForm_existing)

			#educationForm population and edit
			educationData = education.objects.filter(user_id = User_obj)
			if len(educationData) == 0:
				educationData = 'unavailable'
				educationInfoForm = None
			else:
				copy_educationData = educationData
				educationDataCounter = range(len(copy_educationData))
				educationData = zip(copy_educationData, educationDataCounter)
				educationEditForm = []
				for e in copy_educationData:
					e_dict = {
						'tuple_id': e.id,
						'year': e.year,
						'education_type': e.education_type,
						'institution': e.institution_name,
						'aggregate': e.aggregate,
						'what_did_you_do_there': e.what_did_you_do_there
					}
					el = profile_education_add_editForm(e_dict)
					educationEditForm.append(el)
				educationInfoForm = zip(educationEditForm, educationDataCounter)
			educationaddForm = profile_education_add_editForm()

			#workForm population and edit
			workData = work.objects.filter(user_id = User_obj)
			if len(workData) == 0:
				workData = 'unavailable'
				workInfoForm = None
			else:
				copy_workData = workData
				workDataCounter = range(len(copy_workData))
				workData = zip(copy_workData, workDataCounter)
				workEditForm = []
				for w in copy_workData:
					if w.work_type == 'Internship':
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'internship_company_name': w.internship_company_name,
							'internship_from_date': w.internship_date_from,
							'internship_to_date': w.internship_date_to,
							'internship_title': w.internship_title
						}
					elif w.work_type == 'Job':
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'job_company_name': w.job_company_name,
							'job_designation': w.job_designation,
							'job_from_date': w.job_date_from,
							'job_to_date': w.job_date_to
						}
					else:
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'freelancer_client': w.freelancer_client_name,
							'freelancer_project_title': w.freelancer_project_title,
							'freelancer_link': w.freelancer_link,
							'freelancer_project_status': w.freelancer_status,
							'freelancer_year': w.freelancer_year
						}
					wl = profile_work_add_editForm(w_dict)
					workEditForm.append(wl)
				workInfoForm = zip(workEditForm, workDataCounter)
			workaddForm = profile_work_add_editForm()

			#certificationForm populate and edit
			certificationData = certification.objects.filter(user_id = User_obj)
			if len(certificationData) == 0:
				certificationData = 'unavailable'
				certificationInfoForm = None
			else:
				copy_certificationData = certificationData
				certificationDataCounter = range(len(copy_certificationData))
				certificationData = zip(copy_certificationData, certificationDataCounter)
				certificationEditForm = []
				for c in copy_certificationData:
					c_dict = {
						'tuple_id': c.id,
						'year': c.year,
						'agency': c.agency,
						'mode': c.mode_of_certification,
						'details': c.details,					
					}		
					wl = profile_certification_add_editForm(c_dict)
					certificationEditForm.append(wl)
				certificationInfoForm = zip(certificationEditForm, certificationDataCounter)
			certificationaddForm = profile_certification_add_editForm()

			#extracurricularForm populate and edit
			exData = extracurricular_activities.objects.filter(user_id = User_obj)
			if len(exData) == 0:
				exData = 'unavailable'
				exInfoForm = None
			else:
				copy_exData = exData
				exDataCounter = range(len(copy_exData))
				exData = zip(copy_exData, exDataCounter)
				exEditForm = []
				for e in copy_exData:
					e_dict = {
						'tuple_id': e.id,
						'year': e.year,
						'activity_type': e.activity_type,
						'title': e.title,
						'details': e.activity_details,
						'organization': e.organization,
						'link': e.link					
					}			
					wl = profile_extracurricular_add_editForm(e_dict)
					exEditForm.append(wl)
				exInfoForm = zip(exEditForm, exDataCounter)
			extracurricularaddForm = profile_extracurricular_add_editForm()

			#achievementForm populate and edit
			achData = achievements.objects.filter(user_id = User_obj)
			if len(achData) == 0:
				achData = 'unavailable'
				achInfoForm = None
			else:
				copy_achData = achData
				achDataCounter = range(len(copy_achData))
				achData = zip(copy_achData, achDataCounter)
				achEditForm = []
				for a in copy_achData:
					a_dict = {
						'tuple_id': a.id,
						'year': a.year,
						'achievement_type': a.achievement_type,
						'title': a.title,
						'details': a.details,
						'organization': a.organization,
						'link': a.link					
					}			
					wl = profile_achievements_add_editForm(a_dict)
					achEditForm.append(wl)
				achInfoForm = zip(achEditForm, achDataCounter)
			achievementsaddForm = profile_achievements_add_editForm()

			#publicationForm populate and edit
			pubData = publication.objects.filter(user_id = User_obj)
			if len(pubData) == 0:
				pubData = 'unavailable'
				pubInfoForm = None
			else:
				copy_pubData = pubData
				pubDataCounter = range(len(copy_pubData))
				pubData = zip(copy_pubData, pubDataCounter)
				pubEditForm = []
				for p in copy_pubData:
					p_dict = {
						'tuple_id': p.id,
						'year': p.year,
						'mode': p.mode,
						'journal': p.journal,
						'status': p.status,				
						'details': p.details,					
						'link': p.link					
					}			
					wl = profile_publications_add_editForm(p_dict)
					pubEditForm.append(wl)
				pubInfoForm = zip(pubEditForm, pubDataCounter)
			publicationaddForm = profile_publications_add_editForm()

			#patentForm populate and edit
			patData = patent.objects.filter(user_id = User_obj)
			if len(patData) == 0:
				patData = 'unavailable'
				patInfoForm = None
			else:
				copy_patData = patData
				patDataCounter = range(len(copy_patData))
				patData = zip(copy_patData, patDataCounter)
				patEditForm = []
				for pa in copy_patData:
					pa_dict = {
						'tuple_id': pa.id,
						'year': pa.year,
						'mode': pa.mode,					
						'status': pa.patent_status,				
						'details': pa.patent_details
					}			
					wl = profile_patent_add_editForm(pa_dict)
					patEditForm.append(wl)
				patInfoForm = zip(patEditForm, patDataCounter)
			patentaddForm = profile_patent_add_editForm()

			skillsData = skills.objects.filter(user_id = User_obj)
			if len(skillsData) == 0:
				skillsData = 'unavailable'
				skillsInfoForm = None
			else:
				counter = 1
				skill_name_text = ''
				for s in skillsData:
					if counter == 1:
						skill_name_text = s.skill_name
					else:
						skill_name_text = skill_name_text + ',' + s.skill_name
					counter = counter + 1

				s_dict = {
					'skill': skill_name_text
				}
				skillsInfoForm = profile_skills_add_editForm(s_dict)
			skillsaddForm = profile_skills_add_editForm()

			variables = RequestContext(request, {
				'workForm': workForm,
				'educationForm': educationForm,
				'certificationForm': certificationForm,
				'publicationForm': publicationForm,
				'extracurricularForm': extracurricularForm,
				'patentForm': patentForm,
				'achievementForm': achievementForm,
				'aboutForm': aboutForm,
				'educationaddForm': educationaddForm,
				'workaddForm': workaddForm,
				'extracurricularaddForm': extracurricularaddForm,
				'certificationaddForm': certificationaddForm,
				'achievementsaddForm': achievementsaddForm,
				'publicationaddForm': publicationaddForm,
				'patentaddForm': patentaddForm,
				'aboutData': aboutData_existing,
				'educationData': educationData,	
				'educationInfoForm': educationInfoForm,
				'workData': workData,
				'workInfoForm': workInfoForm,
				'certificationData': certificationData,
				'certificationInfoForm': certificationInfoForm,
				'exData': exData,
				'exInfoForm': exInfoForm,
				'achData': achData,
				'achInfoForm': achInfoForm,
				'pubData': pubData,
				'pubInfoForm': pubInfoForm,
				'patData': patData,
				'patInfoForm': patInfoForm,
				'skillsaddForm': skillsaddForm,
				'skillsData': skillsData,
				'skillsInfoForm': skillsInfoForm,
				't_educationData': t_educationData,
				't_workData': t_workData,
				't_certificationData': t_certificationData,
				't_extracurricularData': t_extracurricularData,
				't_achievementData': t_achievementData,
				't_publicationData': t_publicationData,
				't_patentData': t_patentData
			})
			return render_to_response('profile-page.html', variables)

	elif request.method=='GET' and 'patenteditForm' in request.GET:
		patentaddForm = profile_patent_add_editForm(request.GET)
		if patentaddForm.is_valid():
			row_id = patentaddForm.cleaned_data['tuple_id']
			year = patentaddForm.cleaned_data['year']
			mode = patentaddForm.cleaned_data['mode']
			status = patentaddForm.cleaned_data['status']
			details = patentaddForm.cleaned_data['details']

			patent_obj = patent(
				user_id = User_obj,
				year = year,
				mode = mode,
				patent_details = details,
				patent_status = status
			)

			patent_obj = patent.objects.get(id = row_id)

			patent_obj.year = year
			patent_obj.mode = mode
			patent_obj.patent_details = details
			patent_obj.patent_status = status

			patent_obj.save()
			status = {
				'error': False,
				'error_message': '',
				'success': True,
				'success_message': 'Patent details saved.',
			}
			workForm = profile_workForm()
			educationForm = profile_educationForm()
			certificationForm = profile_certificationForm()
			publicationForm = profile_publicationForm()
			extracurricularForm = profile_extracurricularForm()
			patentForm = profile_patentForm()
			achievementForm = profile_achievementForm()
			t_educationData = education.objects.filter(user_id = User_obj)
			if len(t_educationData) == 0:
				t_educationData = 'unavailable'
			else:
				t_educationData = zip(t_educationData, range(len(t_educationData)))
			t_workData = work.objects.filter(user_id = User_obj)
			if len(t_workData) == 0:
				t_workData = 'unavailable'
			else:
				t_workData = zip(t_workData, range(len(t_workData)))
			t_certificationData = certification.objects.filter(user_id = User_obj)
			if len(t_certificationData) == 0:
				t_certificationData = 'unavailable'
			else:
				t_certificationData = zip(t_certificationData, range(len(t_certificationData)))
			t_extracurricularData = extracurricular_activities.objects.filter(user_id = User_obj)
			if len(t_extracurricularData) == 0:
				t_extracurricularData = 'unavailable'
			else:
				t_extracurricularData = zip(t_extracurricularData, range(len(t_extracurricularData)))
			t_achievementData = achievements.objects.filter(user_id = User_obj)
			if len(t_achievementData) == 0:
				t_achievementData = 'unavailable'
			else:
				t_achievementData = zip(t_achievementData, range(len(t_achievementData)))
			t_publicationData = publication.objects.filter(user_id = User_obj)
			if len(t_publicationData) == 0:
				t_publicationData = 'unavailable'
			else:
				t_publicationData = zip(t_publicationData, range(len(t_publicationData)))
			t_patentData = patent.objects.filter(user_id = User_obj)					
			if len(t_patentData) == 0:
				t_patentData = 'unavailable'
			else:
				t_patentData = zip(t_patentData, range(len(t_patentData)))



			# aboutForm population
			try:
				existing_about = user_details.objects.get(user_id = User_obj)
			except:
				existing_about = 'unavailable'
			if existing_about!='unavailable':
				aboutForm_existing = {
					'profession': existing_about.profession,
					'first_name': existing_about.first_name,
					'last_name': existing_about.last_name,
					'dob': existing_about.dob,
					'short_bio': existing_about.short_bio,
					'facebook_url': existing_about.facebook_url,
					'twitter_handle': existing_about.twitter_handle,
					'linkedin_url': existing_about.linkedin_url
				}
			else:
				aboutForm_existing = None
			aboutData_existing = aboutForm_existing
			aboutForm = profile_aboutmeForm(aboutForm_existing)

			#educationForm population and edit
			educationData = education.objects.filter(user_id = User_obj)
			if len(educationData) == 0:
				educationData = 'unavailable'
				educationInfoForm = None
			else:
				copy_educationData = educationData
				educationDataCounter = range(len(copy_educationData))
				educationData = zip(copy_educationData, educationDataCounter)
				educationEditForm = []
				for e in copy_educationData:
					e_dict = {
						'tuple_id': e.id,
						'year': e.year,
						'education_type': e.education_type,
						'institution': e.institution_name,
						'aggregate': e.aggregate,
						'what_did_you_do_there': e.what_did_you_do_there
					}
					el = profile_education_add_editForm(e_dict)
					educationEditForm.append(el)
				educationInfoForm = zip(educationEditForm, educationDataCounter)
			educationaddForm = profile_education_add_editForm()

			#workForm population and edit
			workData = work.objects.filter(user_id = User_obj)
			if len(workData) == 0:
				workData = 'unavailable'
				workInfoForm = None
			else:
				copy_workData = workData
				workDataCounter = range(len(copy_workData))
				workData = zip(copy_workData, workDataCounter)
				workEditForm = []
				for w in copy_workData:
					if w.work_type == 'Internship':
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'internship_company_name': w.internship_company_name,
							'internship_from_date': w.internship_date_from,
							'internship_to_date': w.internship_date_to,
							'internship_title': w.internship_title
						}
					elif w.work_type == 'Job':
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'job_company_name': w.job_company_name,
							'job_designation': w.job_designation,
							'job_from_date': w.job_date_from,
							'job_to_date': w.job_date_to
						}
					else:
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'freelancer_client': w.freelancer_client_name,
							'freelancer_project_title': w.freelancer_project_title,
							'freelancer_link': w.freelancer_link,
							'freelancer_project_status': w.freelancer_status,
							'freelancer_year': w.freelancer_year
						}
					wl = profile_work_add_editForm(w_dict)
					workEditForm.append(wl)
				workInfoForm = zip(workEditForm, workDataCounter)
			workaddForm = profile_work_add_editForm()

			#certificationForm populate and edit
			certificationData = certification.objects.filter(user_id = User_obj)
			if len(certificationData) == 0:
				certificationData = 'unavailable'
				certificationInfoForm = None
			else:
				copy_certificationData = certificationData
				certificationDataCounter = range(len(copy_certificationData))
				certificationData = zip(copy_certificationData, certificationDataCounter)
				certificationEditForm = []
				for c in copy_certificationData:
					c_dict = {
						'tuple_id': c.id,
						'year': c.year,
						'agency': c.agency,
						'mode': c.mode_of_certification,
						'details': c.details,					
					}		
					wl = profile_certification_add_editForm(c_dict)
					certificationEditForm.append(wl)
				certificationInfoForm = zip(certificationEditForm, certificationDataCounter)
			certificationaddForm = profile_certification_add_editForm()

			#extracurricularForm populate and edit
			exData = extracurricular_activities.objects.filter(user_id = User_obj)
			if len(exData) == 0:
				exData = 'unavailable'
				exInfoForm = None
			else:
				copy_exData = exData
				exDataCounter = range(len(copy_exData))
				exData = zip(copy_exData, exDataCounter)
				exEditForm = []
				for e in copy_exData:
					e_dict = {
						'tuple_id': e.id,
						'year': e.year,
						'activity_type': e.activity_type,
						'title': e.title,
						'details': e.activity_details,
						'organization': e.organization,
						'link': e.link					
					}			
					wl = profile_extracurricular_add_editForm(e_dict)
					exEditForm.append(wl)
				exInfoForm = zip(exEditForm, exDataCounter)
			extracurricularaddForm = profile_extracurricular_add_editForm()

			#achievementForm populate and edit
			achData = achievements.objects.filter(user_id = User_obj)
			if len(achData) == 0:
				achData = 'unavailable'
				achInfoForm = None
			else:
				copy_achData = achData
				achDataCounter = range(len(copy_achData))
				achData = zip(copy_achData, achDataCounter)
				achEditForm = []
				for a in copy_achData:
					a_dict = {
						'tuple_id': a.id,
						'year': a.year,
						'achievement_type': a.achievement_type,
						'title': a.title,
						'details': a.details,
						'organization': a.organization,
						'link': a.link					
					}			
					wl = profile_achievements_add_editForm(a_dict)
					achEditForm.append(wl)
				achInfoForm = zip(achEditForm, achDataCounter)
			achievementsaddForm = profile_achievements_add_editForm()

			#publicationForm populate and edit
			pubData = publication.objects.filter(user_id = User_obj)
			if len(pubData) == 0:
				pubData = 'unavailable'
				pubInfoForm = None
			else:
				copy_pubData = pubData
				pubDataCounter = range(len(copy_pubData))
				pubData = zip(copy_pubData, pubDataCounter)
				pubEditForm = []
				for p in copy_pubData:
					p_dict = {
						'tuple_id': p.id,
						'year': p.year,
						'mode': p.mode,
						'journal': p.journal,
						'status': p.status,				
						'details': p.details,					
						'link': p.link					
					}			
					wl = profile_publications_add_editForm(p_dict)
					pubEditForm.append(wl)
				pubInfoForm = zip(pubEditForm, pubDataCounter)
			publicationaddForm = profile_publications_add_editForm()

			#patentForm populate and edit
			patData = patent.objects.filter(user_id = User_obj)
			if len(patData) == 0:
				patData = 'unavailable'
				patInfoForm = None
			else:
				copy_patData = patData
				patDataCounter = range(len(copy_patData))
				patData = zip(copy_patData, patDataCounter)
				patEditForm = []
				for pa in copy_patData:
					pa_dict = {
						'tuple_id': pa.id,
						'year': pa.year,
						'mode': pa.mode,					
						'status': pa.patent_status,				
						'details': pa.patent_details
					}			
					wl = profile_patent_add_editForm(pa_dict)
					patEditForm.append(wl)
				patInfoForm = zip(patEditForm, patDataCounter)
			patentaddForm = profile_patent_add_editForm()

			skillsData = skills.objects.filter(user_id = User_obj)
			if len(skillsData) == 0:
				skillsData = 'unavailable'
				skillsInfoForm = None
			else:
				counter = 1
				skill_name_text = ''
				for s in skillsData:
					if counter == 1:
						skill_name_text = s.skill_name
					else:
						skill_name_text = skill_name_text + ',' + s.skill_name
					counter = counter + 1

				s_dict = {
					'skill': skill_name_text
				}
				skillsInfoForm = profile_skills_add_editForm(s_dict)
			skillsaddForm = profile_skills_add_editForm()

			variables = RequestContext(request, {
				'workForm': workForm,
				'educationForm': educationForm,
				'certificationForm': certificationForm,
				'publicationForm': publicationForm,
				'extracurricularForm': extracurricularForm,
				'patentForm': patentForm,
				'achievementForm': achievementForm,
				'aboutForm': aboutForm,
				'educationaddForm': educationaddForm,
				'workaddForm': workaddForm,
				'extracurricularaddForm': extracurricularaddForm,
				'certificationaddForm': certificationaddForm,
				'achievementsaddForm': achievementsaddForm,
				'publicationaddForm': publicationaddForm,
				'patentaddForm': patentaddForm,
				'aboutData': aboutData_existing,
				'educationData': educationData,	
				'educationInfoForm': educationInfoForm,
				'workData': workData,
				'workInfoForm': workInfoForm,
				'certificationData': certificationData,
				'certificationInfoForm': certificationInfoForm,
				'exData': exData,
				'exInfoForm': exInfoForm,
				'achData': achData,
				'achInfoForm': achInfoForm,
				'pubData': pubData,
				'pubInfoForm': pubInfoForm,
				'patData': patData,
				'patInfoForm': patInfoForm,
				'skillsaddForm': skillsaddForm,
				'skillsData': skillsData,
				'skillsInfoForm': skillsInfoForm,
				't_educationData': t_educationData,
				't_workData': t_workData,
				't_certificationData': t_certificationData,
				't_extracurricularData': t_extracurricularData,
				't_achievementData': t_achievementData,
				't_publicationData': t_publicationData,
				't_patentData': t_patentData
			})
			return render_to_response('profile-page.html', variables)

	elif request.method=='GET' and 'achievementsaddForm' in request.GET:
		achievementsaddForm = profile_achievements_add_editForm(request.GET)
		if achievementsaddForm.is_valid():
			year = achievementsaddForm.cleaned_data['year']
			achievement_type = achievementsaddForm.cleaned_data['achievement_type']
			title = achievementsaddForm.cleaned_data['title']
			organization = achievementsaddForm.cleaned_data['organization']
			details = achievementsaddForm.cleaned_data['details']
			link = achievementsaddForm.cleaned_data['link']
			# attached_file = request.FILES['attach_file']

			achievement_obj = achievements(
				user_id = User_obj,
				year = year,
				achievement_type = achievement_type,
				title = title,
				organization = organization,
				details = details,
				link = link,
				# document = attached_file
			)
			achievement_obj.save()
			status = {
				'error': False,
				'error_message': '',
				'success': True,
				'success_message': 'Achievement details saved.',
			}
			workForm = profile_workForm()
			educationForm = profile_educationForm()
			certificationForm = profile_certificationForm()
			publicationForm = profile_publicationForm()
			extracurricularForm = profile_extracurricularForm()
			patentForm = profile_patentForm()
			achievementForm = profile_achievementForm()
			t_educationData = education.objects.filter(user_id = User_obj)
			if len(t_educationData) == 0:
				t_educationData = 'unavailable'
			else:
				t_educationData = zip(t_educationData, range(len(t_educationData)))
			t_workData = work.objects.filter(user_id = User_obj)
			if len(t_workData) == 0:
				t_workData = 'unavailable'
			else:
				t_workData = zip(t_workData, range(len(t_workData)))
			t_certificationData = certification.objects.filter(user_id = User_obj)
			if len(t_certificationData) == 0:
				t_certificationData = 'unavailable'
			else:
				t_certificationData = zip(t_certificationData, range(len(t_certificationData)))
			t_extracurricularData = extracurricular_activities.objects.filter(user_id = User_obj)
			if len(t_extracurricularData) == 0:
				t_extracurricularData = 'unavailable'
			else:
				t_extracurricularData = zip(t_extracurricularData, range(len(t_extracurricularData)))
			t_achievementData = achievements.objects.filter(user_id = User_obj)
			if len(t_achievementData) == 0:
				t_achievementData = 'unavailable'
			else:
				t_achievementData = zip(t_achievementData, range(len(t_achievementData)))
			t_publicationData = publication.objects.filter(user_id = User_obj)
			if len(t_publicationData) == 0:
				t_publicationData = 'unavailable'
			else:
				t_publicationData = zip(t_publicationData, range(len(t_publicationData)))
			t_patentData = patent.objects.filter(user_id = User_obj)					
			if len(t_patentData) == 0:
				t_patentData = 'unavailable'
			else:
				t_patentData = zip(t_patentData, range(len(t_patentData)))


			
			# aboutForm population
			try:
				existing_about = user_details.objects.get(user_id = User_obj)
			except:
				existing_about = 'unavailable'
			if existing_about!='unavailable':
				aboutForm_existing = {
					'profession': existing_about.profession,
					'first_name': existing_about.first_name,
					'last_name': existing_about.last_name,
					'dob': existing_about.dob,
					'short_bio': existing_about.short_bio,
					'facebook_url': existing_about.facebook_url,
					'twitter_handle': existing_about.twitter_handle,
					'linkedin_url': existing_about.linkedin_url
				}
			else:
				aboutForm_existing = None
			aboutData_existing = aboutForm_existing
			aboutForm = profile_aboutmeForm(aboutForm_existing)

			#educationForm population and edit
			educationData = education.objects.filter(user_id = User_obj)
			if len(educationData) == 0:
				educationData = 'unavailable'
				educationInfoForm = None
			else:
				copy_educationData = educationData
				educationDataCounter = range(len(copy_educationData))
				educationData = zip(copy_educationData, educationDataCounter)
				educationEditForm = []
				for e in copy_educationData:
					e_dict = {
						'tuple_id': e.id,
						'year': e.year,
						'education_type': e.education_type,
						'institution': e.institution_name,
						'aggregate': e.aggregate,
						'what_did_you_do_there': e.what_did_you_do_there
					}
					el = profile_education_add_editForm(e_dict)
					educationEditForm.append(el)
				educationInfoForm = zip(educationEditForm, educationDataCounter)
			educationaddForm = profile_education_add_editForm()

			#workForm population and edit
			workData = work.objects.filter(user_id = User_obj)
			if len(workData) == 0:
				workData = 'unavailable'
				workInfoForm = None
			else:
				copy_workData = workData
				workDataCounter = range(len(copy_workData))
				workData = zip(copy_workData, workDataCounter)
				workEditForm = []
				for w in copy_workData:
					if w.work_type == 'Internship':
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'internship_company_name': w.internship_company_name,
							'internship_from_date': w.internship_date_from,
							'internship_to_date': w.internship_date_to,
							'internship_title': w.internship_title
						}
					elif w.work_type == 'Job':
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'job_company_name': w.job_company_name,
							'job_designation': w.job_designation,
							'job_from_date': w.job_date_from,
							'job_to_date': w.job_date_to
						}
					else:
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'freelancer_client': w.freelancer_client_name,
							'freelancer_project_title': w.freelancer_project_title,
							'freelancer_link': w.freelancer_link,
							'freelancer_project_status': w.freelancer_status,
							'freelancer_year': w.freelancer_year
						}
					wl = profile_work_add_editForm(w_dict)
					workEditForm.append(wl)
				workInfoForm = zip(workEditForm, workDataCounter)
			workaddForm = profile_work_add_editForm()

			#certificationForm populate and edit
			certificationData = certification.objects.filter(user_id = User_obj)
			if len(certificationData) == 0:
				certificationData = 'unavailable'
				certificationInfoForm = None
			else:
				copy_certificationData = certificationData
				certificationDataCounter = range(len(copy_certificationData))
				certificationData = zip(copy_certificationData, certificationDataCounter)
				certificationEditForm = []
				for c in copy_certificationData:
					c_dict = {
						'tuple_id': c.id,
						'year': c.year,
						'agency': c.agency,
						'mode': c.mode_of_certification,
						'details': c.details,					
					}		
					wl = profile_certification_add_editForm(c_dict)
					certificationEditForm.append(wl)
				certificationInfoForm = zip(certificationEditForm, certificationDataCounter)
			certificationaddForm = profile_certification_add_editForm()

			#extracurricularForm populate and edit
			exData = extracurricular_activities.objects.filter(user_id = User_obj)
			if len(exData) == 0:
				exData = 'unavailable'
				exInfoForm = None
			else:
				copy_exData = exData
				exDataCounter = range(len(copy_exData))
				exData = zip(copy_exData, exDataCounter)
				exEditForm = []
				for e in copy_exData:
					e_dict = {
						'tuple_id': e.id,
						'year': e.year,
						'activity_type': e.activity_type,
						'title': e.title,
						'details': e.activity_details,
						'organization': e.organization,
						'link': e.link					
					}			
					wl = profile_extracurricular_add_editForm(e_dict)
					exEditForm.append(wl)
				exInfoForm = zip(exEditForm, exDataCounter)
			extracurricularaddForm = profile_extracurricular_add_editForm()

			#achievementForm populate and edit
			achData = achievements.objects.filter(user_id = User_obj)
			if len(achData) == 0:
				achData = 'unavailable'
				achInfoForm = None
			else:
				copy_achData = achData
				achDataCounter = range(len(copy_achData))
				achData = zip(copy_achData, achDataCounter)
				achEditForm = []
				for a in copy_achData:
					a_dict = {
						'tuple_id': a.id,
						'year': a.year,
						'achievement_type': a.achievement_type,
						'title': a.title,
						'details': a.details,
						'organization': a.organization,
						'link': a.link					
					}			
					wl = profile_achievements_add_editForm(a_dict)
					achEditForm.append(wl)
				achInfoForm = zip(achEditForm, achDataCounter)
			achievementsaddForm = profile_achievements_add_editForm()

			#publicationForm populate and edit
			pubData = publication.objects.filter(user_id = User_obj)
			if len(pubData) == 0:
				pubData = 'unavailable'
				pubInfoForm = None
			else:
				copy_pubData = pubData
				pubDataCounter = range(len(copy_pubData))
				pubData = zip(copy_pubData, pubDataCounter)
				pubEditForm = []
				for p in copy_pubData:
					p_dict = {
						'tuple_id': p.id,
						'year': p.year,
						'mode': p.mode,
						'journal': p.journal,
						'status': p.status,				
						'details': p.details,					
						'link': p.link					
					}			
					wl = profile_publications_add_editForm(p_dict)
					pubEditForm.append(wl)
				pubInfoForm = zip(pubEditForm, pubDataCounter)
			publicationaddForm = profile_publications_add_editForm()

			#patentForm populate and edit
			patData = patent.objects.filter(user_id = User_obj)
			if len(patData) == 0:
				patData = 'unavailable'
				patInfoForm = None
			else:
				copy_patData = patData
				patDataCounter = range(len(copy_patData))
				patData = zip(copy_patData, patDataCounter)
				patEditForm = []
				for pa in copy_patData:
					pa_dict = {
						'tuple_id': pa.id,						
						'year': pa.year,
						'mode': pa.mode,					
						'status': pa.patent_status,				
						'details': pa.patent_details
					}			
					wl = profile_patent_add_editForm(pa_dict)
					patEditForm.append(wl)
				patInfoForm = zip(patEditForm, patDataCounter)
			patentaddForm = profile_patent_add_editForm()

			skillsData = skills.objects.filter(user_id = User_obj)
			if len(skillsData) == 0:
				skillsData = 'unavailable'
				skillsInfoForm = None
			else:
				counter = 1
				skill_name_text = ''
				for s in skillsData:
					if counter == 1:
						skill_name_text = s.skill_name
					else:
						skill_name_text = skill_name_text + ',' + s.skill_name
					counter = counter + 1

				s_dict = {
					'skill': skill_name_text
				}
				skillsInfoForm = profile_skills_add_editForm(s_dict)
			skillsaddForm = profile_skills_add_editForm()

			variables = RequestContext(request, {
				'workForm': workForm,
				'educationForm': educationForm,
				'certificationForm': certificationForm,
				'publicationForm': publicationForm,
				'extracurricularForm': extracurricularForm,
				'patentForm': patentForm,
				'achievementForm': achievementForm,
				'aboutForm': aboutForm,
				'educationaddForm': educationaddForm,
				'workaddForm': workaddForm,
				'extracurricularaddForm': extracurricularaddForm,
				'certificationaddForm': certificationaddForm,
				'achievementsaddForm': achievementsaddForm,
				'publicationaddForm': publicationaddForm,
				'patentaddForm': patentaddForm,
				'aboutData': aboutData_existing,
				'educationData': educationData,	
				'educationInfoForm': educationInfoForm,
				'workData': workData,
				'workInfoForm': workInfoForm,
				'certificationData': certificationData,
				'certificationInfoForm': certificationInfoForm,
				'exData': exData,
				'exInfoForm': exInfoForm,
				'achData': achData,
				'achInfoForm': achInfoForm,
				'pubData': pubData,
				'pubInfoForm': pubInfoForm,
				'patData': patData,
				'patInfoForm': patInfoForm,
				'skillsaddForm': skillsaddForm,
				'skillsData': skillsData,
				'skillsInfoForm': skillsInfoForm,
				't_educationData': t_educationData,
				't_workData': t_workData,
				't_certificationData': t_certificationData,
				't_extracurricularData': t_extracurricularData,
				't_achievementData': t_achievementData,
				't_publicationData': t_publicationData,
				't_patentData': t_patentData
			})
			return render_to_response('profile-page.html', variables)

	elif request.method=='GET' and 'achievementseditForm' in request.GET:
		achievementsaddForm = profile_achievements_add_editForm(request.GET)
		if achievementsaddForm.is_valid():
			row_id = achievementsaddForm.cleaned_data['tuple_id']
			year = achievementsaddForm.cleaned_data['year']
			achievement_type = achievementsaddForm.cleaned_data['achievement_type']
			title = achievementsaddForm.cleaned_data['title']
			organization = achievementsaddForm.cleaned_data['organization']
			details = achievementsaddForm.cleaned_data['details']
			link = achievementsaddForm.cleaned_data['link']
			# attached_file = request.FILES['attach_file']

			achievement_obj = achievements(
				user_id = User_obj,
				year = year,
				achievement_type = achievement_type,
				title = title,
				organization = organization,
				details = details,
				link = link,
				# document = attached_file
			)

			achievement_obj = achievements.objects.get(id = row_id)

			achievement_obj.year = year
			achievement_obj.achievement_type = achievement_type
			achievement_obj.title = title
			achievement_obj.organization = organization
			achievement_obj.details = details
			achievement_obj.link = link

			achievement_obj.save()
			status = {
				'error': False,
				'error_message': '',
				'success': True,
				'success_message': 'Achievement details saved.',
			}
			workForm = profile_workForm()
			educationForm = profile_educationForm()
			certificationForm = profile_certificationForm()
			publicationForm = profile_publicationForm()
			extracurricularForm = profile_extracurricularForm()
			patentForm = profile_patentForm()
			achievementForm = profile_achievementForm()
			t_educationData = education.objects.filter(user_id = User_obj)
			if len(t_educationData) == 0:
				t_educationData = 'unavailable'
			else:
				t_educationData = zip(t_educationData, range(len(t_educationData)))
			t_workData = work.objects.filter(user_id = User_obj)
			if len(t_workData) == 0:
				t_workData = 'unavailable'
			else:
				t_workData = zip(t_workData, range(len(t_workData)))
			t_certificationData = certification.objects.filter(user_id = User_obj)
			if len(t_certificationData) == 0:
				t_certificationData = 'unavailable'
			else:
				t_certificationData = zip(t_certificationData, range(len(t_certificationData)))
			t_extracurricularData = extracurricular_activities.objects.filter(user_id = User_obj)
			if len(t_extracurricularData) == 0:
				t_extracurricularData = 'unavailable'
			else:
				t_extracurricularData = zip(t_extracurricularData, range(len(t_extracurricularData)))
			t_achievementData = achievements.objects.filter(user_id = User_obj)
			if len(t_achievementData) == 0:
				t_achievementData = 'unavailable'
			else:
				t_achievementData = zip(t_achievementData, range(len(t_achievementData)))
			t_publicationData = publication.objects.filter(user_id = User_obj)
			if len(t_publicationData) == 0:
				t_publicationData = 'unavailable'
			else:
				t_publicationData = zip(t_publicationData, range(len(t_publicationData)))
			t_patentData = patent.objects.filter(user_id = User_obj)					
			if len(t_patentData) == 0:
				t_patentData = 'unavailable'
			else:
				t_patentData = zip(t_patentData, range(len(t_patentData)))


			
			# aboutForm population
			try:
				existing_about = user_details.objects.get(user_id = User_obj)
			except:
				existing_about = 'unavailable'
			if existing_about!='unavailable':
				aboutForm_existing = {
					'profession': existing_about.profession,
					'first_name': existing_about.first_name,
					'last_name': existing_about.last_name,
					'dob': existing_about.dob,
					'short_bio': existing_about.short_bio,
					'facebook_url': existing_about.facebook_url,
					'twitter_handle': existing_about.twitter_handle,
					'linkedin_url': existing_about.linkedin_url
				}
			else:
				aboutForm_existing = None
			aboutData_existing = aboutForm_existing
			aboutForm = profile_aboutmeForm(aboutForm_existing)

			#educationForm population and edit
			educationData = education.objects.filter(user_id = User_obj)
			if len(educationData) == 0:
				educationData = 'unavailable'
				educationInfoForm = None
			else:
				copy_educationData = educationData
				educationDataCounter = range(len(copy_educationData))
				educationData = zip(copy_educationData, educationDataCounter)
				educationEditForm = []
				for e in copy_educationData:
					e_dict = {
						'tuple_id': e.id,
						'year': e.year,
						'education_type': e.education_type,
						'institution': e.institution_name,
						'aggregate': e.aggregate,
						'what_did_you_do_there': e.what_did_you_do_there
					}
					el = profile_education_add_editForm(e_dict)
					educationEditForm.append(el)
				educationInfoForm = zip(educationEditForm, educationDataCounter)
			educationaddForm = profile_education_add_editForm()

			#workForm population and edit
			workData = work.objects.filter(user_id = User_obj)
			if len(workData) == 0:
				workData = 'unavailable'
				workInfoForm = None
			else:
				copy_workData = workData
				workDataCounter = range(len(copy_workData))
				workData = zip(copy_workData, workDataCounter)
				workEditForm = []
				for w in copy_workData:
					if w.work_type == 'Internship':
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'internship_company_name': w.internship_company_name,
							'internship_from_date': w.internship_date_from,
							'internship_to_date': w.internship_date_to,
							'internship_title': w.internship_title
						}
					elif w.work_type == 'Job':
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'job_company_name': w.job_company_name,
							'job_designation': w.job_designation,
							'job_from_date': w.job_date_from,
							'job_to_date': w.job_date_to
						}
					else:
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'freelancer_client': w.freelancer_client_name,
							'freelancer_project_title': w.freelancer_project_title,
							'freelancer_link': w.freelancer_link,
							'freelancer_project_status': w.freelancer_status,
							'freelancer_year': w.freelancer_year
						}
					wl = profile_work_add_editForm(w_dict)
					workEditForm.append(wl)
				workInfoForm = zip(workEditForm, workDataCounter)
			workaddForm = profile_work_add_editForm()

			#certificationForm populate and edit
			certificationData = certification.objects.filter(user_id = User_obj)
			if len(certificationData) == 0:
				certificationData = 'unavailable'
				certificationInfoForm = None
			else:
				copy_certificationData = certificationData
				certificationDataCounter = range(len(copy_certificationData))
				certificationData = zip(copy_certificationData, certificationDataCounter)
				certificationEditForm = []
				for c in copy_certificationData:
					c_dict = {
						'tuple_id': c.id,
						'year': c.year,
						'agency': c.agency,
						'mode': c.mode_of_certification,
						'details': c.details,					
					}		
					wl = profile_certification_add_editForm(c_dict)
					certificationEditForm.append(wl)
				certificationInfoForm = zip(certificationEditForm, certificationDataCounter)
			certificationaddForm = profile_certification_add_editForm()

			#extracurricularForm populate and edit
			exData = extracurricular_activities.objects.filter(user_id = User_obj)
			if len(exData) == 0:
				exData = 'unavailable'
				exInfoForm = None
			else:
				copy_exData = exData
				exDataCounter = range(len(copy_exData))
				exData = zip(copy_exData, exDataCounter)
				exEditForm = []
				for e in copy_exData:
					e_dict = {
						'tuple_id': e.id,
						'year': e.year,
						'activity_type': e.activity_type,
						'title': e.title,
						'details': e.activity_details,
						'organization': e.organization,
						'link': e.link					
					}			
					wl = profile_extracurricular_add_editForm(e_dict)
					exEditForm.append(wl)
				exInfoForm = zip(exEditForm, exDataCounter)
			extracurricularaddForm = profile_extracurricular_add_editForm()

			#achievementForm populate and edit
			achData = achievements.objects.filter(user_id = User_obj)
			if len(achData) == 0:
				achData = 'unavailable'
				achInfoForm = None
			else:
				copy_achData = achData
				achDataCounter = range(len(copy_achData))
				achData = zip(copy_achData, achDataCounter)
				achEditForm = []
				for a in copy_achData:
					a_dict = {
						'tuple_id': a.id,
						'year': a.year,
						'achievement_type': a.achievement_type,
						'title': a.title,
						'details': a.details,
						'organization': a.organization,
						'link': a.link					
					}			
					wl = profile_achievements_add_editForm(a_dict)
					achEditForm.append(wl)
				achInfoForm = zip(achEditForm, achDataCounter)
			achievementsaddForm = profile_achievements_add_editForm()

			#publicationForm populate and edit
			pubData = publication.objects.filter(user_id = User_obj)
			if len(pubData) == 0:
				pubData = 'unavailable'
				pubInfoForm = None
			else:
				copy_pubData = pubData
				pubDataCounter = range(len(copy_pubData))
				pubData = zip(copy_pubData, pubDataCounter)
				pubEditForm = []
				for p in copy_pubData:
					p_dict = {
						'tuple_id': p.id,
						'year': p.year,
						'mode': p.mode,
						'journal': p.journal,
						'status': p.status,				
						'details': p.details,					
						'link': p.link					
					}			
					wl = profile_publications_add_editForm(p_dict)
					pubEditForm.append(wl)
				pubInfoForm = zip(pubEditForm, pubDataCounter)
			publicationaddForm = profile_publications_add_editForm()

			#patentForm populate and edit
			patData = patent.objects.filter(user_id = User_obj)
			if len(patData) == 0:
				patData = 'unavailable'
				patInfoForm = None
			else:
				copy_patData = patData
				patDataCounter = range(len(copy_patData))
				patData = zip(copy_patData, patDataCounter)
				patEditForm = []
				for pa in copy_patData:
					pa_dict = {
						'tuple_id': pa.id,						
						'year': pa.year,
						'mode': pa.mode,					
						'status': pa.patent_status,				
						'details': pa.patent_details
					}			
					wl = profile_patent_add_editForm(pa_dict)
					patEditForm.append(wl)
				patInfoForm = zip(patEditForm, patDataCounter)
			patentaddForm = profile_patent_add_editForm()

			skillsData = skills.objects.filter(user_id = User_obj)
			if len(skillsData) == 0:
				skillsData = 'unavailable'
				skillsInfoForm = None
			else:
				counter = 1
				skill_name_text = ''
				for s in skillsData:
					if counter == 1:
						skill_name_text = s.skill_name
					else:
						skill_name_text = skill_name_text + ',' + s.skill_name
					counter = counter + 1

				s_dict = {
					'skill': skill_name_text
				}
				skillsInfoForm = profile_skills_add_editForm(s_dict)
			skillsaddForm = profile_skills_add_editForm()

			variables = RequestContext(request, {
				'workForm': workForm,
				'educationForm': educationForm,
				'certificationForm': certificationForm,
				'publicationForm': publicationForm,
				'extracurricularForm': extracurricularForm,
				'patentForm': patentForm,
				'achievementForm': achievementForm,
				'aboutForm': aboutForm,
				'educationaddForm': educationaddForm,
				'workaddForm': workaddForm,
				'extracurricularaddForm': extracurricularaddForm,
				'certificationaddForm': certificationaddForm,
				'achievementsaddForm': achievementsaddForm,
				'publicationaddForm': publicationaddForm,
				'patentaddForm': patentaddForm,
				'aboutData': aboutData_existing,
				'educationData': educationData,	
				'educationInfoForm': educationInfoForm,
				'workData': workData,
				'workInfoForm': workInfoForm,
				'certificationData': certificationData,
				'certificationInfoForm': certificationInfoForm,
				'exData': exData,
				'exInfoForm': exInfoForm,
				'achData': achData,
				'achInfoForm': achInfoForm,
				'pubData': pubData,
				'pubInfoForm': pubInfoForm,
				'patData': patData,
				'patInfoForm': patInfoForm,
				'skillsaddForm': skillsaddForm,
				'skillsData': skillsData,
				'skillsInfoForm': skillsInfoForm,
				't_educationData': t_educationData,
				't_workData': t_workData,
				't_certificationData': t_certificationData,
				't_extracurricularData': t_extracurricularData,
				't_achievementData': t_achievementData,
				't_publicationData': t_publicationData,
				't_patentData': t_patentData
			})
			return render_to_response('profile-page.html', variables)

	elif request.method=='GET' and 'achievementsdeleteForm' in request.GET:
		achievementsaddForm = profile_achievements_add_editForm(request.GET)
		if achievementsaddForm.is_valid():
			row_id = achievementsaddForm.cleaned_data['tuple_id']
			year = achievementsaddForm.cleaned_data['year']
			achievement_type = achievementsaddForm.cleaned_data['achievement_type']
			title = achievementsaddForm.cleaned_data['title']
			organization = achievementsaddForm.cleaned_data['organization']
			details = achievementsaddForm.cleaned_data['details']
			link = achievementsaddForm.cleaned_data['link']
			# attached_file = request.FILES['attach_file']

			achievement_obj = achievements.objects.get(id = row_id)

			achievement_obj.delete()
			status = {
				'error': False,
				'error_message': '',
				'success': True,
				'success_message': 'Achievement details deleted.',
			}
			workForm = profile_workForm()
			educationForm = profile_educationForm()
			certificationForm = profile_certificationForm()
			publicationForm = profile_publicationForm()
			extracurricularForm = profile_extracurricularForm()
			patentForm = profile_patentForm()
			achievementForm = profile_achievementForm()
			t_educationData = education.objects.filter(user_id = User_obj)
			if len(t_educationData) == 0:
				t_educationData = 'unavailable'
			else:
				t_educationData = zip(t_educationData, range(len(t_educationData)))
			t_workData = work.objects.filter(user_id = User_obj)
			if len(t_workData) == 0:
				t_workData = 'unavailable'
			else:
				t_workData = zip(t_workData, range(len(t_workData)))
			t_certificationData = certification.objects.filter(user_id = User_obj)
			if len(t_certificationData) == 0:
				t_certificationData = 'unavailable'
			else:
				t_certificationData = zip(t_certificationData, range(len(t_certificationData)))
			t_extracurricularData = extracurricular_activities.objects.filter(user_id = User_obj)
			if len(t_extracurricularData) == 0:
				t_extracurricularData = 'unavailable'
			else:
				t_extracurricularData = zip(t_extracurricularData, range(len(t_extracurricularData)))
			t_achievementData = achievements.objects.filter(user_id = User_obj)
			if len(t_achievementData) == 0:
				t_achievementData = 'unavailable'
			else:
				t_achievementData = zip(t_achievementData, range(len(t_achievementData)))
			t_publicationData = publication.objects.filter(user_id = User_obj)
			if len(t_publicationData) == 0:
				t_publicationData = 'unavailable'
			else:
				t_publicationData = zip(t_publicationData, range(len(t_publicationData)))
			t_patentData = patent.objects.filter(user_id = User_obj)					
			if len(t_patentData) == 0:
				t_patentData = 'unavailable'
			else:
				t_patentData = zip(t_patentData, range(len(t_patentData)))


			
			# aboutForm population
			try:
				existing_about = user_details.objects.get(user_id = User_obj)
			except:
				existing_about = 'unavailable'
			if existing_about!='unavailable':
				aboutForm_existing = {
					'profession': existing_about.profession,
					'first_name': existing_about.first_name,
					'last_name': existing_about.last_name,
					'dob': existing_about.dob,
					'short_bio': existing_about.short_bio,
					'facebook_url': existing_about.facebook_url,
					'twitter_handle': existing_about.twitter_handle,
					'linkedin_url': existing_about.linkedin_url
				}
			else:
				aboutForm_existing = None
			aboutData_existing = aboutForm_existing
			aboutForm = profile_aboutmeForm(aboutForm_existing)

			#educationForm population and edit
			educationData = education.objects.filter(user_id = User_obj)
			if len(educationData) == 0:
				educationData = 'unavailable'
				educationInfoForm = None
			else:
				copy_educationData = educationData
				educationDataCounter = range(len(copy_educationData))
				educationData = zip(copy_educationData, educationDataCounter)
				educationEditForm = []
				for e in copy_educationData:
					e_dict = {
						'tuple_id': e.id,
						'year': e.year,
						'education_type': e.education_type,
						'institution': e.institution_name,
						'aggregate': e.aggregate,
						'what_did_you_do_there': e.what_did_you_do_there
					}
					el = profile_education_add_editForm(e_dict)
					educationEditForm.append(el)
				educationInfoForm = zip(educationEditForm, educationDataCounter)
			educationaddForm = profile_education_add_editForm()

			#workForm population and edit
			workData = work.objects.filter(user_id = User_obj)
			if len(workData) == 0:
				workData = 'unavailable'
				workInfoForm = None
			else:
				copy_workData = workData
				workDataCounter = range(len(copy_workData))
				workData = zip(copy_workData, workDataCounter)
				workEditForm = []
				for w in copy_workData:
					if w.work_type == 'Internship':
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'internship_company_name': w.internship_company_name,
							'internship_from_date': w.internship_date_from,
							'internship_to_date': w.internship_date_to,
							'internship_title': w.internship_title
						}
					elif w.work_type == 'Job':
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'job_company_name': w.job_company_name,
							'job_designation': w.job_designation,
							'job_from_date': w.job_date_from,
							'job_to_date': w.job_date_to
						}
					else:
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'freelancer_client': w.freelancer_client_name,
							'freelancer_project_title': w.freelancer_project_title,
							'freelancer_link': w.freelancer_link,
							'freelancer_project_status': w.freelancer_status,
							'freelancer_year': w.freelancer_year
						}
					wl = profile_work_add_editForm(w_dict)
					workEditForm.append(wl)
				workInfoForm = zip(workEditForm, workDataCounter)
			workaddForm = profile_work_add_editForm()

			#certificationForm populate and edit
			certificationData = certification.objects.filter(user_id = User_obj)
			if len(certificationData) == 0:
				certificationData = 'unavailable'
				certificationInfoForm = None
			else:
				copy_certificationData = certificationData
				certificationDataCounter = range(len(copy_certificationData))
				certificationData = zip(copy_certificationData, certificationDataCounter)
				certificationEditForm = []
				for c in copy_certificationData:
					c_dict = {
						'tuple_id': c.id,
						'year': c.year,
						'agency': c.agency,
						'mode': c.mode_of_certification,
						'details': c.details,					
					}		
					wl = profile_certification_add_editForm(c_dict)
					certificationEditForm.append(wl)
				certificationInfoForm = zip(certificationEditForm, certificationDataCounter)
			certificationaddForm = profile_certification_add_editForm()

			#extracurricularForm populate and edit
			exData = extracurricular_activities.objects.filter(user_id = User_obj)
			if len(exData) == 0:
				exData = 'unavailable'
				exInfoForm = None
			else:
				copy_exData = exData
				exDataCounter = range(len(copy_exData))
				exData = zip(copy_exData, exDataCounter)
				exEditForm = []
				for e in copy_exData:
					e_dict = {
						'tuple_id': e.id,
						'year': e.year,
						'activity_type': e.activity_type,
						'title': e.title,
						'details': e.activity_details,
						'organization': e.organization,
						'link': e.link					
					}			
					wl = profile_extracurricular_add_editForm(e_dict)
					exEditForm.append(wl)
				exInfoForm = zip(exEditForm, exDataCounter)
			extracurricularaddForm = profile_extracurricular_add_editForm()

			#achievementForm populate and edit
			achData = achievements.objects.filter(user_id = User_obj)
			if len(achData) == 0:
				achData = 'unavailable'
				achInfoForm = None
			else:
				copy_achData = achData
				achDataCounter = range(len(copy_achData))
				achData = zip(copy_achData, achDataCounter)
				achEditForm = []
				for a in copy_achData:
					a_dict = {
						'tuple_id': a.id,
						'year': a.year,
						'achievement_type': a.achievement_type,
						'title': a.title,
						'details': a.details,
						'organization': a.organization,
						'link': a.link					
					}			
					wl = profile_achievements_add_editForm(a_dict)
					achEditForm.append(wl)
				achInfoForm = zip(achEditForm, achDataCounter)
			achievementsaddForm = profile_achievements_add_editForm()

			#publicationForm populate and edit
			pubData = publication.objects.filter(user_id = User_obj)
			if len(pubData) == 0:
				pubData = 'unavailable'
				pubInfoForm = None
			else:
				copy_pubData = pubData
				pubDataCounter = range(len(copy_pubData))
				pubData = zip(copy_pubData, pubDataCounter)
				pubEditForm = []
				for p in copy_pubData:
					p_dict = {
						'tuple_id': p.id,
						'year': p.year,
						'mode': p.mode,
						'journal': p.journal,
						'status': p.status,				
						'details': p.details,					
						'link': p.link					
					}			
					wl = profile_publications_add_editForm(p_dict)
					pubEditForm.append(wl)
				pubInfoForm = zip(pubEditForm, pubDataCounter)
			publicationaddForm = profile_publications_add_editForm()

			#patentForm populate and edit
			patData = patent.objects.filter(user_id = User_obj)
			if len(patData) == 0:
				patData = 'unavailable'
				patInfoForm = None
			else:
				copy_patData = patData
				patDataCounter = range(len(copy_patData))
				patData = zip(copy_patData, patDataCounter)
				patEditForm = []
				for pa in copy_patData:
					pa_dict = {
						'tuple_id': pa.id,						
						'year': pa.year,
						'mode': pa.mode,					
						'status': pa.patent_status,				
						'details': pa.patent_details
					}			
					wl = profile_patent_add_editForm(pa_dict)
					patEditForm.append(wl)
				patInfoForm = zip(patEditForm, patDataCounter)
			patentaddForm = profile_patent_add_editForm()

			skillsData = skills.objects.filter(user_id = User_obj)
			if len(skillsData) == 0:
				skillsData = 'unavailable'
				skillsInfoForm = None
			else:
				counter = 1
				skill_name_text = ''
				for s in skillsData:
					if counter == 1:
						skill_name_text = s.skill_name
					else:
						skill_name_text = skill_name_text + ',' + s.skill_name
					counter = counter + 1

				s_dict = {
					'skill': skill_name_text
				}
				skillsInfoForm = profile_skills_add_editForm(s_dict)
			skillsaddForm = profile_skills_add_editForm()

			variables = RequestContext(request, {
				'workForm': workForm,
				'educationForm': educationForm,
				'certificationForm': certificationForm,
				'publicationForm': publicationForm,
				'extracurricularForm': extracurricularForm,
				'patentForm': patentForm,
				'achievementForm': achievementForm,
				'aboutForm': aboutForm,
				'educationaddForm': educationaddForm,
				'workaddForm': workaddForm,
				'extracurricularaddForm': extracurricularaddForm,
				'certificationaddForm': certificationaddForm,
				'achievementsaddForm': achievementsaddForm,
				'publicationaddForm': publicationaddForm,
				'patentaddForm': patentaddForm,
				'aboutData': aboutData_existing,
				'educationData': educationData,	
				'educationInfoForm': educationInfoForm,
				'workData': workData,
				'workInfoForm': workInfoForm,
				'certificationData': certificationData,
				'certificationInfoForm': certificationInfoForm,
				'exData': exData,
				'exInfoForm': exInfoForm,
				'achData': achData,
				'achInfoForm': achInfoForm,
				'pubData': pubData,
				'pubInfoForm': pubInfoForm,
				'patData': patData,
				'patInfoForm': patInfoForm,
				'skillsaddForm': skillsaddForm,
				'skillsData': skillsData,
				'skillsInfoForm': skillsInfoForm,
				't_educationData': t_educationData,
				't_workData': t_workData,
				't_certificationData': t_certificationData,
				't_extracurricularData': t_extracurricularData,
				't_achievementData': t_achievementData,
				't_publicationData': t_publicationData,
				't_patentData': t_patentData
			})
			return render_to_response('profile-page.html', variables)

	elif request.method=='GET' and 'aboutForm' in request.GET:
		aboutForm = profile_aboutmeForm(request.GET)
		if aboutForm.is_valid():
			first_name = aboutForm.cleaned_data['first_name']
			last_name = aboutForm.cleaned_data['last_name']
			dob = aboutForm.cleaned_data['dob']
			profession = aboutForm.cleaned_data['profession']
			short_bio = aboutForm.cleaned_data['short_bio']
			facebook_url = aboutForm.cleaned_data['facebook_url']
			twitter_handle = aboutForm.cleaned_data['twitter_handle']
			linkedin_url = aboutForm.cleaned_data['linkedin_url']

			formatted_dob = dob[6:] +'-'+ dob[0:2] +'-'+ dob[3:5]

			existing_user_details_obj = user_details.objects.get(user_id=User_obj)

			existing_user_details_obj.first_name = first_name
			existing_user_details_obj.last_name = last_name
			existing_user_details_obj.profession = profession
			existing_user_details_obj.dob = formatted_dob
			existing_user_details_obj.short_bio = short_bio
			existing_user_details_obj.twitter_handle = twitter_handle
			existing_user_details_obj.facebook_url = facebook_url
			existing_user_details_obj.linkedin_url = linkedin_url

			existing_user_details_obj.save()
			status = {
				'error': False,
				'error_message': '',
				'success': True,
				'success_message': 'About Me details saved.',
			}
			aboutForm_existing = {
				'profession': existing_user_details_obj.profession,
				'first_name': existing_user_details_obj.first_name,
				'last_name': existing_user_details_obj.last_name,
				'dob': existing_user_details_obj.dob,
				'short_bio': existing_user_details_obj.short_bio,
				'facebook_url': existing_user_details_obj.facebook_url,
				'twitter_handle': existing_user_details_obj.twitter_handle,
				'linkedin_url': existing_user_details_obj.linkedin_url
			}
			workForm = profile_workForm()
			educationForm = profile_educationForm()
			certificationForm = profile_certificationForm()
			publicationForm = profile_publicationForm()
			extracurricularForm = profile_extracurricularForm()
			patentForm = profile_patentForm()
			achievementForm = profile_achievementForm()
			t_educationData = education.objects.filter(user_id = User_obj)
			if len(t_educationData) == 0:
				t_educationData = 'unavailable'
			else:
				t_educationData = zip(t_educationData, range(len(t_educationData)))
			t_workData = work.objects.filter(user_id = User_obj)
			if len(t_workData) == 0:
				t_workData = 'unavailable'
			else:
				t_workData = zip(t_workData, range(len(t_workData)))
			t_certificationData = certification.objects.filter(user_id = User_obj)
			if len(t_certificationData) == 0:
				t_certificationData = 'unavailable'
			else:
				t_certificationData = zip(t_certificationData, range(len(t_certificationData)))
			t_extracurricularData = extracurricular_activities.objects.filter(user_id = User_obj)
			if len(t_extracurricularData) == 0:
				t_extracurricularData = 'unavailable'
			else:
				t_extracurricularData = zip(t_extracurricularData, range(len(t_extracurricularData)))
			t_achievementData = achievements.objects.filter(user_id = User_obj)
			if len(t_achievementData) == 0:
				t_achievementData = 'unavailable'
			else:
				t_achievementData = zip(t_achievementData, range(len(t_achievementData)))
			t_publicationData = publication.objects.filter(user_id = User_obj)
			if len(t_publicationData) == 0:
				t_publicationData = 'unavailable'
			else:
				t_publicationData = zip(t_publicationData, range(len(t_publicationData)))
			t_patentData = patent.objects.filter(user_id = User_obj)					
			if len(t_patentData) == 0:
				t_patentData = 'unavailable'
			else:
				t_patentData = zip(t_patentData, range(len(t_patentData)))


			
			# aboutForm population
			try:
				existing_about = user_details.objects.get(user_id = User_obj)
			except:
				existing_about = 'unavailable'
			if existing_about!='unavailable':
				aboutForm_existing = {
					'profession': existing_about.profession,
					'first_name': existing_about.first_name,
					'last_name': existing_about.last_name,
					'dob': existing_about.dob,
					'short_bio': existing_about.short_bio,
					'facebook_url': existing_about.facebook_url,
					'twitter_handle': existing_about.twitter_handle,
					'linkedin_url': existing_about.linkedin_url
				}
			else:
				aboutForm_existing = None
			aboutData_existing = aboutForm_existing
			aboutForm = profile_aboutmeForm(aboutForm_existing)

			#educationForm population and edit
			educationData = education.objects.filter(user_id = User_obj)
			if len(educationData) == 0:
				educationData = 'unavailable'
				educationInfoForm = None
			else:
				copy_educationData = educationData
				educationDataCounter = range(len(copy_educationData))
				educationData = zip(copy_educationData, educationDataCounter)
				educationEditForm = []
				for e in copy_educationData:
					e_dict = {
						'tuple_id': e.id,
						'year': e.year,
						'education_type': e.education_type,
						'institution': e.institution_name,
						'aggregate': e.aggregate,
						'what_did_you_do_there': e.what_did_you_do_there
					}
					el = profile_education_add_editForm(e_dict)
					educationEditForm.append(el)
				educationInfoForm = zip(educationEditForm, educationDataCounter)
			educationaddForm = profile_education_add_editForm()

			#workForm population and edit
			workData = work.objects.filter(user_id = User_obj)
			if len(workData) == 0:
				workData = 'unavailable'
				workInfoForm = None
			else:
				copy_workData = workData
				workDataCounter = range(len(copy_workData))
				workData = zip(copy_workData, workDataCounter)
				workEditForm = []
				for w in copy_workData:
					if w.work_type == 'Internship':
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'internship_company_name': w.internship_company_name,
							'internship_from_date': w.internship_date_from,
							'internship_to_date': w.internship_date_to,
							'internship_title': w.internship_title
						}
					elif w.work_type == 'Job':
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'job_company_name': w.job_company_name,
							'job_designation': w.job_designation,
							'job_from_date': w.job_date_from,
							'job_to_date': w.job_date_to
						}
					else:
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'freelancer_client': w.freelancer_client_name,
							'freelancer_project_title': w.freelancer_project_title,
							'freelancer_link': w.freelancer_link,
							'freelancer_project_status': w.freelancer_status,
							'freelancer_year': w.freelancer_year
						}
					wl = profile_work_add_editForm(w_dict)
					workEditForm.append(wl)
				workInfoForm = zip(workEditForm, workDataCounter)
			workaddForm = profile_work_add_editForm()

			#certificationForm populate and edit
			certificationData = certification.objects.filter(user_id = User_obj)
			if len(certificationData) == 0:
				certificationData = 'unavailable'
				certificationInfoForm = None
			else:
				copy_certificationData = certificationData
				certificationDataCounter = range(len(copy_certificationData))
				certificationData = zip(copy_certificationData, certificationDataCounter)
				certificationEditForm = []
				for c in copy_certificationData:
					c_dict = {
						'tuple_id': c.id,
						'year': c.year,
						'agency': c.agency,
						'mode': c.mode_of_certification,
						'details': c.details,					
					}		
					wl = profile_certification_add_editForm(c_dict)
					certificationEditForm.append(wl)
				certificationInfoForm = zip(certificationEditForm, certificationDataCounter)
			certificationaddForm = profile_certification_add_editForm()

			#extracurricularForm populate and edit
			exData = extracurricular_activities.objects.filter(user_id = User_obj)
			if len(exData) == 0:
				exData = 'unavailable'
				exInfoForm = None
			else:
				copy_exData = exData
				exDataCounter = range(len(copy_exData))
				exData = zip(copy_exData, exDataCounter)
				exEditForm = []
				for e in copy_exData:
					e_dict = {
						'tuple_id': e.id,
						'year': e.year,
						'activity_type': e.activity_type,
						'title': e.title,
						'details': e.activity_details,
						'organization': e.organization,
						'link': e.link					
					}			
					wl = profile_extracurricular_add_editForm(e_dict)
					exEditForm.append(wl)
				exInfoForm = zip(exEditForm, exDataCounter)
			extracurricularaddForm = profile_extracurricular_add_editForm()

			#achievementForm populate and edit
			achData = achievements.objects.filter(user_id = User_obj)
			if len(achData) == 0:
				achData = 'unavailable'
				achInfoForm = None
			else:
				copy_achData = achData
				achDataCounter = range(len(copy_achData))
				achData = zip(copy_achData, achDataCounter)
				achEditForm = []
				for a in copy_achData:
					a_dict = {
						'tuple_id': a.id,
						'year': a.year,
						'achievement_type': a.achievement_type,
						'title': a.title,
						'details': a.details,
						'organization': a.organization,
						'link': a.link					
					}			
					wl = profile_achievements_add_editForm(a_dict)
					achEditForm.append(wl)
				achInfoForm = zip(achEditForm, achDataCounter)
			achievementsaddForm = profile_achievements_add_editForm()

			#publicationForm populate and edit
			pubData = publication.objects.filter(user_id = User_obj)
			if len(pubData) == 0:
				pubData = 'unavailable'
				pubInfoForm = None
			else:
				copy_pubData = pubData
				pubDataCounter = range(len(copy_pubData))
				pubData = zip(copy_pubData, pubDataCounter)
				pubEditForm = []
				for p in copy_pubData:
					p_dict = {
						'tuple_id': p.id,
						'year': p.year,
						'mode': p.mode,
						'journal': p.journal,
						'status': p.status,				
						'details': p.details,					
						'link': p.link					
					}			
					wl = profile_publications_add_editForm(p_dict)
					pubEditForm.append(wl)
				pubInfoForm = zip(pubEditForm, pubDataCounter)
			publicationaddForm = profile_publications_add_editForm()

			#patentForm populate and edit
			patData = patent.objects.filter(user_id = User_obj)
			if len(patData) == 0:
				patData = 'unavailable'
				patInfoForm = None
			else:
				copy_patData = patData
				patDataCounter = range(len(copy_patData))
				patData = zip(copy_patData, patDataCounter)
				patEditForm = []
				for pa in copy_patData:
					pa_dict = {
						'tuple_id': pa.id,
						'year': pa.year,
						'mode': pa.mode,					
						'status': pa.patent_status,				
						'details': pa.patent_details
					}			
					wl = profile_patent_add_editForm(pa_dict)
					patEditForm.append(wl)
				patInfoForm = zip(patEditForm, patDataCounter)
			patentaddForm = profile_patent_add_editForm()

			skillsData = skills.objects.filter(user_id = User_obj)
			if len(skillsData) == 0:
				skillsData = 'unavailable'
				skillsInfoForm = None
			else:
				counter = 1
				skill_name_text = ''
				for s in skillsData:
					if counter == 1:
						skill_name_text = s.skill_name
					else:
						skill_name_text = skill_name_text + ',' + s.skill_name
					counter = counter + 1

				s_dict = {
					'skill': skill_name_text
				}
				skillsInfoForm = profile_skills_add_editForm(s_dict)
			skillsaddForm = profile_skills_add_editForm()

			variables = RequestContext(request, {
				'workForm': workForm,
				'educationForm': educationForm,
				'certificationForm': certificationForm,
				'publicationForm': publicationForm,
				'extracurricularForm': extracurricularForm,
				'patentForm': patentForm,
				'achievementForm': achievementForm,
				'aboutForm': aboutForm,
				'educationaddForm': educationaddForm,
				'workaddForm': workaddForm,
				'extracurricularaddForm': extracurricularaddForm,
				'certificationaddForm': certificationaddForm,
				'achievementsaddForm': achievementsaddForm,
				'publicationaddForm': publicationaddForm,
				'patentaddForm': patentaddForm,
				'aboutData': aboutData_existing,
				'educationData': educationData,	
				'educationInfoForm': educationInfoForm,
				'workData': workData,
				'workInfoForm': workInfoForm,
				'certificationData': certificationData,
				'certificationInfoForm': certificationInfoForm,
				'exData': exData,
				'exInfoForm': exInfoForm,
				'achData': achData,
				'achInfoForm': achInfoForm,
				'pubData': pubData,
				'pubInfoForm': pubInfoForm,
				'patData': patData,
				'patInfoForm': patInfoForm,
				'skillsaddForm': skillsaddForm,
				'skillsData': skillsData,
				'skillsInfoForm': skillsInfoForm,
				't_educationData': t_educationData,
				't_workData': t_workData,
				't_certificationData': t_certificationData,
				't_extracurricularData': t_extracurricularData,
				't_achievementData': t_achievementData,
				't_publicationData': t_publicationData,
				't_patentData': t_patentData
			})
			return render_to_response('profile-page.html', variables)

	elif request.method == 'GET' and 'skillsaddForm' in request.GET:
		skillsaddForm = profile_skills_add_editForm(request.GET)
		if skillsaddForm.is_valid():
			skill = skillsaddForm.cleaned_data['skill']
			skill_set = skill.split(',')
			for s in skill_set:
				skills_obj = skills(
					user_id = User_obj,
					skill_name = s
				)
				skills_obj.save()

			status = {
				'error': False,
				'error_message': '',
				'success': True,
				'success_message': 'Skills saved.',
			}
			workForm = profile_workForm()
			educationForm = profile_educationForm()
			certificationForm = profile_certificationForm()
			publicationForm = profile_publicationForm()
			extracurricularForm = profile_extracurricularForm()
			patentForm = profile_patentForm()
			achievementForm = profile_achievementForm()
			t_educationData = education.objects.filter(user_id = User_obj)
			if len(t_educationData) == 0:
				t_educationData = 'unavailable'
			else:
				t_educationData = zip(t_educationData, range(len(t_educationData)))
			t_workData = work.objects.filter(user_id = User_obj)
			if len(t_workData) == 0:
				t_workData = 'unavailable'
			else:
				t_workData = zip(t_workData, range(len(t_workData)))
			t_certificationData = certification.objects.filter(user_id = User_obj)
			if len(t_certificationData) == 0:
				t_certificationData = 'unavailable'
			else:
				t_certificationData = zip(t_certificationData, range(len(t_certificationData)))
			t_extracurricularData = extracurricular_activities.objects.filter(user_id = User_obj)
			if len(t_extracurricularData) == 0:
				t_extracurricularData = 'unavailable'
			else:
				t_extracurricularData = zip(t_extracurricularData, range(len(t_extracurricularData)))
			t_achievementData = achievements.objects.filter(user_id = User_obj)
			if len(t_achievementData) == 0:
				t_achievementData = 'unavailable'
			else:
				t_achievementData = zip(t_achievementData, range(len(t_achievementData)))
			t_publicationData = publication.objects.filter(user_id = User_obj)
			if len(t_publicationData) == 0:
				t_publicationData = 'unavailable'
			else:
				t_publicationData = zip(t_publicationData, range(len(t_publicationData)))
			t_patentData = patent.objects.filter(user_id = User_obj)					
			if len(t_patentData) == 0:
				t_patentData = 'unavailable'
			else:
				t_patentData = zip(t_patentData, range(len(t_patentData)))


			
			# aboutForm population
			try:
				existing_about = user_details.objects.get(user_id = User_obj)
			except:
				existing_about = 'unavailable'
			if existing_about!='unavailable':
				aboutForm_existing = {
					'profession': existing_about.profession,
					'first_name': existing_about.first_name,
					'last_name': existing_about.last_name,
					'dob': existing_about.dob,
					'short_bio': existing_about.short_bio,
					'facebook_url': existing_about.facebook_url,
					'twitter_handle': existing_about.twitter_handle,
					'linkedin_url': existing_about.linkedin_url
				}
			else:
				aboutForm_existing = None
			aboutData_existing = aboutForm_existing
			aboutForm = profile_aboutmeForm(aboutForm_existing)

			#educationForm population and edit
			educationData = education.objects.filter(user_id = User_obj)
			if len(educationData) == 0:
				educationData = 'unavailable'
				educationInfoForm = None
			else:
				copy_educationData = educationData
				educationDataCounter = range(len(copy_educationData))
				educationData = zip(copy_educationData, educationDataCounter)
				educationEditForm = []
				for e in copy_educationData:
					e_dict = {
						'tuple_id': e.id,
						'year': e.year,
						'education_type': e.education_type,
						'institution': e.institution_name,
						'aggregate': e.aggregate,
						'what_did_you_do_there': e.what_did_you_do_there
					}
					el = profile_education_add_editForm(e_dict)
					educationEditForm.append(el)
				educationInfoForm = zip(educationEditForm, educationDataCounter)
			educationaddForm = profile_education_add_editForm()

			#workForm population and edit
			workData = work.objects.filter(user_id = User_obj)
			if len(workData) == 0:
				workData = 'unavailable'
				workInfoForm = None
			else:
				copy_workData = workData
				workDataCounter = range(len(copy_workData))
				workData = zip(copy_workData, workDataCounter)
				workEditForm = []
				for w in copy_workData:
					if w.work_type == 'Internship':
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'internship_company_name': w.internship_company_name,
							'internship_from_date': w.internship_date_from,
							'internship_to_date': w.internship_date_to,
							'internship_title': w.internship_title
						}
					elif w.work_type == 'Job':
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'job_company_name': w.job_company_name,
							'job_designation': w.job_designation,
							'job_from_date': w.job_date_from,
							'job_to_date': w.job_date_to
						}
					else:
						w_dict = {
							'tuple_id': w.id,
							'work_type': w.work_type,
							'freelancer_client': w.freelancer_client_name,
							'freelancer_project_title': w.freelancer_project_title,
							'freelancer_link': w.freelancer_link,
							'freelancer_project_status': w.freelancer_status,
							'freelancer_year': w.freelancer_year
						}
					wl = profile_work_add_editForm(w_dict)
					workEditForm.append(wl)
				workInfoForm = zip(workEditForm, workDataCounter)
			workaddForm = profile_work_add_editForm()

			#certificationForm populate and edit
			certificationData = certification.objects.filter(user_id = User_obj)
			if len(certificationData) == 0:
				certificationData = 'unavailable'
				certificationInfoForm = None
			else:
				copy_certificationData = certificationData
				certificationDataCounter = range(len(copy_certificationData))
				certificationData = zip(copy_certificationData, certificationDataCounter)
				certificationEditForm = []
				for c in copy_certificationData:
					c_dict = {
						'tuple_id': c.id,
						'year': c.year,
						'agency': c.agency,
						'mode': c.mode_of_certification,
						'details': c.details,					
					}		
					wl = profile_certification_add_editForm(c_dict)
					certificationEditForm.append(wl)
				certificationInfoForm = zip(certificationEditForm, certificationDataCounter)
			certificationaddForm = profile_certification_add_editForm()

			#extracurricularForm populate and edit
			exData = extracurricular_activities.objects.filter(user_id = User_obj)
			if len(exData) == 0:
				exData = 'unavailable'
				exInfoForm = None
			else:
				copy_exData = exData
				exDataCounter = range(len(copy_exData))
				exData = zip(copy_exData, exDataCounter)
				exEditForm = []
				for e in copy_exData:
					e_dict = {
						'tuple_id': e.id,
						'year': e.year,
						'activity_type': e.activity_type,
						'title': e.title,
						'details': e.activity_details,
						'organization': e.organization,
						'link': e.link					
					}			
					wl = profile_extracurricular_add_editForm(e_dict)
					exEditForm.append(wl)
				exInfoForm = zip(exEditForm, exDataCounter)
			extracurricularaddForm = profile_extracurricular_add_editForm()

			#achievementForm populate and edit
			achData = achievements.objects.filter(user_id = User_obj)
			if len(achData) == 0:
				achData = 'unavailable'
				achInfoForm = None
			else:
				copy_achData = achData
				achDataCounter = range(len(copy_achData))
				achData = zip(copy_achData, achDataCounter)
				achEditForm = []
				for a in copy_achData:
					a_dict = {
						'tuple_id': a.id,
						'year': a.year,
						'achievement_type': a.achievement_type,
						'title': a.title,
						'details': a.details,
						'organization': a.organization,
						'link': a.link					
					}			
					wl = profile_achievements_add_editForm(a_dict)
					achEditForm.append(wl)
				achInfoForm = zip(achEditForm, achDataCounter)
			achievementsaddForm = profile_achievements_add_editForm()

			#publicationForm populate and edit
			pubData = publication.objects.filter(user_id = User_obj)
			if len(pubData) == 0:
				pubData = 'unavailable'
				pubInfoForm = None
			else:
				copy_pubData = pubData
				pubDataCounter = range(len(copy_pubData))
				pubData = zip(copy_pubData, pubDataCounter)
				pubEditForm = []
				for p in copy_pubData:
					p_dict = {
						'tuple_id': p.id,
						'year': p.year,
						'mode': p.mode,
						'journal': p.journal,
						'status': p.status,				
						'details': p.details,					
						'link': p.link					
					}			
					wl = profile_publications_add_editForm(p_dict)
					pubEditForm.append(wl)
				pubInfoForm = zip(pubEditForm, pubDataCounter)
			publicationaddForm = profile_publications_add_editForm()

			#patentForm populate and edit
			patData = patent.objects.filter(user_id = User_obj)
			if len(patData) == 0:
				patData = 'unavailable'
				patInfoForm = None
			else:
				copy_patData = patData
				patDataCounter = range(len(copy_patData))
				patData = zip(copy_patData, patDataCounter)
				patEditForm = []
				for pa in copy_patData:
					pa_dict = {
						'tuple_id': pa.id,
						'year': pa.year,
						'mode': pa.mode,					
						'status': pa.patent_status,				
						'details': pa.patent_details
					}			
					wl = profile_patent_add_editForm(pa_dict)
					patEditForm.append(wl)
				patInfoForm = zip(patEditForm, patDataCounter)
			patentaddForm = profile_patent_add_editForm()

			skillsData = skills.objects.filter(user_id = User_obj)
			if len(skillsData) == 0:
				skillsData = 'unavailable'
				skillsInfoForm = None
			else:
				counter = 1
				skill_name_text = ''
				for s in skillsData:
					if counter == 1:
						skill_name_text = s.skill_name
					else:
						skill_name_text = skill_name_text + ',' + s.skill_name
					counter = counter + 1

				s_dict = {
					'skill': skill_name_text
				}
				skillsInfoForm = profile_skills_add_editForm(s_dict)
			skillsaddForm = profile_skills_add_editForm()

			variables = RequestContext(request, {
				'workForm': workForm,
				'educationForm': educationForm,
				'certificationForm': certificationForm,
				'publicationForm': publicationForm,
				'extracurricularForm': extracurricularForm,
				'patentForm': patentForm,
				'achievementForm': achievementForm,
				'aboutForm': aboutForm,
				'educationaddForm': educationaddForm,
				'workaddForm': workaddForm,
				'extracurricularaddForm': extracurricularaddForm,
				'certificationaddForm': certificationaddForm,
				'achievementsaddForm': achievementsaddForm,
				'publicationaddForm': publicationaddForm,
				'patentaddForm': patentaddForm,
				'aboutData': aboutData_existing,
				'educationData': educationData,	
				'educationInfoForm': educationInfoForm,
				'workData': workData,
				'workInfoForm': workInfoForm,
				'certificationData': certificationData,
				'certificationInfoForm': certificationInfoForm,
				'exData': exData,
				'exInfoForm': exInfoForm,
				'achData': achData,
				'achInfoForm': achInfoForm,
				'pubData': pubData,
				'pubInfoForm': pubInfoForm,
				'patData': patData,
				'patInfoForm': patInfoForm,
				'skillsaddForm': skillsaddForm,
				'skillsData': skillsData,
				'skillsInfoForm': skillsInfoForm,
				't_educationData': t_educationData,
				't_workData': t_workData,
				't_certificationData': t_certificationData,
				't_extracurricularData': t_extracurricularData,
				't_achievementData': t_achievementData,
				't_publicationData': t_publicationData,
				't_patentData': t_patentData
			})
			return render_to_response('profile-page.html', variables)			

	else:
		workForm = profile_workForm()
		educationForm = profile_educationForm()
		certificationForm = profile_certificationForm()
		publicationForm = profile_publicationForm()
		extracurricularForm = profile_extracurricularForm()
		patentForm = profile_patentForm()
		achievementForm = profile_achievementForm()
		t_educationData = education.objects.filter(user_id = User_obj)
		if len(t_educationData) == 0:
			t_educationData = 'unavailable'
		else:
			t_educationData = zip(t_educationData, range(len(t_educationData)))
		t_workData = work.objects.filter(user_id = User_obj)
		if len(t_workData) == 0:
			t_workData = 'unavailable'
		else:
			t_workData = zip(t_workData, range(len(t_workData)))
		t_certificationData = certification.objects.filter(user_id = User_obj)
		if len(t_certificationData) == 0:
			t_certificationData = 'unavailable'
		else:
			t_certificationData = zip(t_certificationData, range(len(t_certificationData)))
		t_extracurricularData = extracurricular_activities.objects.filter(user_id = User_obj)
		if len(t_extracurricularData) == 0:
			t_extracurricularData = 'unavailable'
		else:
			t_extracurricularData = zip(t_extracurricularData, range(len(t_extracurricularData)))
		t_achievementData = achievements.objects.filter(user_id = User_obj)
		if len(t_achievementData) == 0:
			t_achievementData = 'unavailable'
		else:
			t_achievementData = zip(t_achievementData, range(len(t_achievementData)))
		t_publicationData = publication.objects.filter(user_id = User_obj)
		if len(t_publicationData) == 0:
			t_publicationData = 'unavailable'
		else:
			t_publicationData = zip(t_publicationData, range(len(t_publicationData)))
		t_patentData = patent.objects.filter(user_id = User_obj)					
		if len(t_patentData) == 0:
			t_patentData = 'unavailable'
		else:
			t_patentData = zip(t_patentData, range(len(t_patentData)))


		
		# aboutForm population
		try:
			existing_about = user_details.objects.get(user_id = User_obj)
		except:
			existing_about = 'unavailable'
		if existing_about!='unavailable':
			aboutForm_existing = {
				'profession': existing_about.profession,
				'first_name': existing_about.first_name,
				'last_name': existing_about.last_name,
				'dob': existing_about.dob,
				'short_bio': existing_about.short_bio,
				'facebook_url': existing_about.facebook_url,
				'twitter_handle': existing_about.twitter_handle,
				'linkedin_url': existing_about.linkedin_url
			}
		else:
			aboutForm_existing = None
		aboutData_existing = aboutForm_existing
		aboutForm = profile_aboutmeForm(aboutForm_existing)

		#educationForm population and edit
		educationData = education.objects.filter(user_id = User_obj)
		if len(educationData) == 0:
			educationData = 'unavailable'
			educationInfoForm = None
		else:
			copy_educationData = educationData
			educationDataCounter = range(len(copy_educationData))
			educationData = zip(copy_educationData, educationDataCounter)
			educationEditForm = []
			for e in copy_educationData:
				e_dict = {
					'tuple_id': e.id,
					'year': e.year,
					'education_type': e.education_type,
					'institution': e.institution_name,
					'aggregate': e.aggregate,
					'what_did_you_do_there': e.what_did_you_do_there
				}
				el = profile_education_add_editForm(e_dict)
				educationEditForm.append(el)
			educationInfoForm = zip(educationEditForm, educationDataCounter)
		educationaddForm = profile_education_add_editForm()

		#workForm population and edit
		workData = work.objects.filter(user_id = User_obj)
		if len(workData) == 0:
			workData = 'unavailable'
			workInfoForm = None
		else:
			copy_workData = workData
			workDataCounter = range(len(copy_workData))
			workData = zip(copy_workData, workDataCounter)
			workEditForm = []
			for w in copy_workData:
				if w.work_type == 'Internship':
					w_dict = {
						'tuple_id': w.id,
						'work_type': w.work_type,
						'internship_company_name': w.internship_company_name,
						'internship_from_date': w.internship_date_from,
						'internship_to_date': w.internship_date_to,
						'internship_title': w.internship_title
					}
				elif w.work_type == 'Job':
					w_dict = {
						'tuple_id': w.id,
						'work_type': w.work_type,
						'job_company_name': w.job_company_name,
						'job_designation': w.job_designation,
						'job_from_date': w.job_date_from,
						'job_to_date': w.job_date_to
					}
				else:
					w_dict = {
						'tuple_id': w.id,
						'work_type': w.work_type,
						'freelancer_client': w.freelancer_client_name,
						'freelancer_project_title': w.freelancer_project_title,
						'freelancer_link': w.freelancer_link,
						'freelancer_project_status': w.freelancer_status,
						'freelancer_year': w.freelancer_year
					}
				wl = profile_work_add_editForm(w_dict)
				workEditForm.append(wl)
			workInfoForm = zip(workEditForm, workDataCounter)
		workaddForm = profile_work_add_editForm()

		#certificationForm populate and edit
		certificationData = certification.objects.filter(user_id = User_obj)
		if len(certificationData) == 0:
			certificationData = 'unavailable'
			certificationInfoForm = None
		else:
			copy_certificationData = certificationData
			certificationDataCounter = range(len(copy_certificationData))
			certificationData = zip(copy_certificationData, certificationDataCounter)
			certificationEditForm = []
			for c in copy_certificationData:
				c_dict = {
					'tuple_id': c.id,
					'year': c.year,
					'agency': c.agency,
					'mode': c.mode_of_certification,
					'details': c.details,					
				}		
				wl = profile_certification_add_editForm(c_dict)
				certificationEditForm.append(wl)
			certificationInfoForm = zip(certificationEditForm, certificationDataCounter)
		certificationaddForm = profile_certification_add_editForm()

		#extracurricularForm populate and edit
		exData = extracurricular_activities.objects.filter(user_id = User_obj)
		if len(exData) == 0:
			exData = 'unavailable'
			exInfoForm = None
		else:
			copy_exData = exData
			exDataCounter = range(len(copy_exData))
			exData = zip(copy_exData, exDataCounter)
			exEditForm = []
			for e in copy_exData:
				e_dict = {
					'tuple_id': e.id,
					'year': e.year,
					'activity_type': e.activity_type,
					'title': e.title,
					'details': e.activity_details,
					'organization': e.organization,
					'link': e.link					
				}			
				wl = profile_extracurricular_add_editForm(e_dict)
				exEditForm.append(wl)
			exInfoForm = zip(exEditForm, exDataCounter)
		extracurricularaddForm = profile_extracurricular_add_editForm()

		#achievementForm populate and edit
		achData = achievements.objects.filter(user_id = User_obj)
		if len(achData) == 0:
			achData = 'unavailable'
			achInfoForm = None
		else:
			copy_achData = achData
			achDataCounter = range(len(copy_achData))
			achData = zip(copy_achData, achDataCounter)
			achEditForm = []
			for a in copy_achData:
				a_dict = {
					'tuple_id': a.id,
					'year': a.year,
					'achievement_type': a.achievement_type,
					'title': a.title,
					'details': a.details,
					'organization': a.organization,
					'link': a.link					
				}			
				wl = profile_achievements_add_editForm(a_dict)
				achEditForm.append(wl)
			achInfoForm = zip(achEditForm, achDataCounter)
		achievementsaddForm = profile_achievements_add_editForm()

		#publicationForm populate and edit
		pubData = publication.objects.filter(user_id = User_obj)
		if len(pubData) == 0:
			pubData = 'unavailable'
			pubInfoForm = None
		else:
			copy_pubData = pubData
			pubDataCounter = range(len(copy_pubData))
			pubData = zip(copy_pubData, pubDataCounter)
			pubEditForm = []
			for p in copy_pubData:
				p_dict = {
					'tuple_id': p.id,
					'year': p.year,
					'mode': p.mode,
					'journal': p.journal,
					'status': p.status,				
					'details': p.details,					
					'link': p.link					
				}			
				wl = profile_publications_add_editForm(p_dict)
				pubEditForm.append(wl)
			pubInfoForm = zip(pubEditForm, pubDataCounter)
		publicationaddForm = profile_publications_add_editForm()

		#patentForm populate and edit
		patData = patent.objects.filter(user_id = User_obj)
		if len(patData) == 0:
			patData = 'unavailable'
			patInfoForm = None
		else:
			copy_patData = patData
			patDataCounter = range(len(copy_patData))
			patData = zip(copy_patData, patDataCounter)
			patEditForm = []
			for pa in copy_patData:
				pa_dict = {
					'tuple_id': pa.id,
					'year': pa.year,
					'mode': pa.mode,					
					'status': pa.patent_status,				
					'details': pa.patent_details
				}			
				wl = profile_patent_add_editForm(pa_dict)
				patEditForm.append(wl)
			patInfoForm = zip(patEditForm, patDataCounter)
		patentaddForm = profile_patent_add_editForm()

		#skillsForm populate and edit
		skillsData = skills.objects.filter(user_id = User_obj)
		if len(skillsData) == 0:
			skillsData = 'unavailable'
			skillsInfoForm = None
		else:
			counter = 1
			skill_name_text = ''
			for s in skillsData:
				if counter == 1:
					skill_name_text = s.skill_name
				else:
					skill_name_text = skill_name_text + ',' + s.skill_name
				counter = counter + 1

			s_dict = {
				'skill': skill_name_text
			}
			skillsInfoForm = profile_skills_add_editForm(s_dict)
		skillsaddForm = profile_skills_add_editForm()

		variables = RequestContext(request, {
			'workForm': workForm,
			'educationForm': educationForm,
			'certificationForm': certificationForm,
			'publicationForm': publicationForm,
			'extracurricularForm': extracurricularForm,
			'patentForm': patentForm,
			'achievementForm': achievementForm,
			'aboutForm': aboutForm,
			'educationaddForm': educationaddForm,
			'workaddForm': workaddForm,
			'extracurricularaddForm': extracurricularaddForm,
			'certificationaddForm': certificationaddForm,
			'achievementsaddForm': achievementsaddForm,
			'publicationaddForm': publicationaddForm,
			'patentaddForm': patentaddForm,
			'aboutData': aboutData_existing,
			'educationData': educationData,	
			'educationInfoForm': educationInfoForm,
			'workData': workData,
			'workInfoForm': workInfoForm,
			'certificationData': certificationData,
			'certificationInfoForm': certificationInfoForm,
			'exData': exData,
			'exInfoForm': exInfoForm,
			'achData': achData,
			'achInfoForm': achInfoForm,
			'pubData': pubData,
			'pubInfoForm': pubInfoForm,
			'patData': patData,
			'patInfoForm': patInfoForm,
			'skillsaddForm': skillsaddForm,
			'skillsData': skillsData,
			'skillsInfoForm': skillsInfoForm,
			't_educationData': t_educationData,
			't_workData': t_workData,
			't_certificationData': t_certificationData,
			't_extracurricularData': t_extracurricularData,
			't_achievementData': t_achievementData,
			't_publicationData': t_publicationData,
			't_patentData': t_patentData
		})
		return render_to_response('profile-page.html', variables)

def logoutPage(request):
	logout(request)
	return HttpResponseRedirect('/login/')