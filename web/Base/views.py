from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from Login.models import User, User_request
from django.core.mail import send_mail
from Base.models import License

def home(request):

	if 'auth' in request.session:
		auth_session = request.session['auth']
	else:
		auth_session = False
	if 'approver' in request.session:
		approver_session = request.session['approver']
	else:
		approver_session = False

	if auth_session == True:
		template  = loader.get_template('Base/home.html') 
		context   = RequestContext(request, {
			'auth_session' 		: auth_session,
			'approver_session' 	: approver_session,
		})
		return HttpResponse(template.render(context))
	else:
		return HttpResponseRedirect('/login')
	


def view_licenses(request):
	if 'auth' in request.session:
		auth_session = request.session['auth']
	else:
		auth_session = False
	if 'approver' in request.session:
		approver_session = request.session['approver']
	else:
		approver_session = False

	license_list = []
	for license in License.objects.order_by('date_requested'):
		if license.authorization == "accepted":
			a = '_license'
			b = str(license.software_name)
			c = b+a
			c = [license.software_name, license.software_version, license.license_type, license.date_requested]
			license_list.append(c)



	template  = loader.get_template('Base/view_licenses.html') 
	context   = RequestContext(request, {
		'auth_session' 		: auth_session,
		'approver_session' 	: approver_session,
		'license_list'		: license_list,
	})
	return HttpResponse(template.render(context))



def license_detail(request, license_name, license_version):
	if 'auth' in request.session:
		auth_session = request.session['auth']
	else:
		auth_session = False
	if 'approver' in request.session:
		approver_session = request.session['approver']
	else:
		approver_session = False

	template  = loader.get_template('Base/license_detail.html') 
	context   = RequestContext(request, {
		'auth_session' : auth_session,
		'approver_session' 	: approver_session,
	})
	return HttpResponse(template.render(context))



def request_form(request):
	if 'auth' in request.session:
		auth_session = request.session['auth']
	else:
		auth_session = False
	if 'approver' in request.session:
		approver_session = request.session['approver']
	else:
		approver_session = False

	if 'request_error' in request.session:
		request_error = request.session['request_error']
		del request.session['request_error']
	else:
		request_error = False

	template  = loader.get_template('Base/request_form.html') 
	context   = RequestContext(request, {
		'auth_session' : auth_session,
		'approver_session' 	: approver_session,
		'error' : request_error,
	})
	return HttpResponse(template.render(context))

def intermediate_logic(request):
	software_name 		= request.POST['software_name']
	software_version 	= request.POST['software_version']

	license_name_list = []
	license_list = License.objects.all()
	for license in license_list:
		if license.authorization == 'accepted':
			a = license.software_name+"_"+license.software_version
			license_name_list.append(a)
	b = software_name+"_"+software_version


	if not software_name or not software_version:
		request.session['request_error'] = 'You did not enter the software name and/or version. Please fill out both boxes.'
		return HttpResponseRedirect('/submit_request')

	elif b in license_name_list:
		request.session['request_error'] = 'There is an existing accepted request for this software and version.'
		return HttpResponseRedirect('/submit_request')

	else:
		return HttpResponseRedirect('/submit_request/'+software_name+'_version_'+software_version+'/')



def additional_information(request, license_name, license_version):
	if 'auth' in request.session:
		auth_session = request.session['auth']
	else:
		auth_session = False
	if 'approver' in request.session:
		approver_session = request.session['approver']
	else:
		approver_session = False

	username = request.session['current_user']
	user = User.objects.get(username = username)
	user_f_name = user.first_name
	user_l_name = user.last_name

	template  = loader.get_template('Base/request_form_cont.html') 
	context   = RequestContext(request, {
		'current_user_first': user_f_name,
		'current_user_last': user_l_name,
		'auth_session' 		: auth_session,
		'approver_session' 	: approver_session,
		'software_name' 	: license_name,
		'software_version' 	: license_version,
	})
	return HttpResponse(template.render(context))

def request_sent(request):
	if 'auth' in request.session:
		auth_session = request.session['auth']
	else:
		auth_session = False
	if 'approver' in request.session:
		approver_session = request.session['approver']
	else:
		approver_session = False

	licensor_name 		= request.POST['licensor_name']
	license_type 		= request.POST['license_type']
	copy_of_license 	= request.POST['copy_of_license']
	where_used 			= request.POST['where_used']
	client_where_used	= request.POST['client_where_used']
	desc_nature_work	= request.POST['desc_nature_work']
	desc_function_work 	= request.POST['desc_function_work']
	category_of_work 	= request.POST['category_of_work']
	if_ML_paid_for 		= request.POST.get('if_ML_paid_for', False)
	ML_pay_twenfivk 	= request.POST.get('ML_pay_twenfivk', False)
	ongoing_payments	= request.POST.get('ongoing_payments', False)
	if ongoing_payments:	
		ongoing_how_much 	= request.POST['ongoing_how_much']
		ongoing_how_often 	= request.POST['ongoing_how_often']
	we_use_work 		= request.POST.get('we_use_work', False)
	do_we_distribute 	= request.POST['do_we_distribute']
	did_we_host 		= request.POST.get('did_we_host', False)
	third_party_host 	= request.POST.get('third_party_host', False)
	if_modified 		= request.POST.get('if_modified', False)
	use_generate_code 	= request.POST.get('use_generate_code', False)
	form_gen_code 		= request.POST['form_gen_code']
	how_hard_replace 	= request.POST['how_hard_replace']
	obligation 			= request.POST.get('obligation', False)
	additional_comments = request.POST['additional_comments']
	software_name 		= request.POST['software_name']
	software_version 	= request.POST['software_version']
	requested_by_first	= request.POST['requested_by_first']
	requested_by_last	= request.POST['requested_by_last']

	if ongoing_payments == False:
		ongoing_how_much = 0
		ongoing_how_often = 0
	elif ongoing_payments:
		if not ongoing_how_much or not ongoing_how_often:
			return HttpResponse("One or more fields was left blank. Please press your browser's 'back' button and check all boxes.")

	requested_by = requested_by_first+" "+requested_by_last

	if not licensor_name or not license_type or not copy_of_license or not where_used or not client_where_used or not desc_nature_work or not desc_function_work or not category_of_work or not do_we_distribute or not form_gen_code or not how_hard_replace or not additional_comments or not software_name or not software_version:
		return HttpResponse("One or more fields was left blank. Please press your browser's 'back' button and check all boxes.")

	if approver_session == True:
		authorization = 'accepted'
	else:
		authorization = 'none'


	new_license = License(licensor_name = licensor_name, license_type = license_type, copy_of_license = copy_of_license, where_used = where_used, client_where_used = client_where_used, 
						  desc_nature_work = desc_nature_work, desc_function_work = desc_function_work, category_of_work = category_of_work, if_ML_paid_for = if_ML_paid_for, 
						  ML_pay_twenfivk = ML_pay_twenfivk, ongoing_payments = ongoing_payments, ongoing_how_much = ongoing_how_much, ongoing_how_often = ongoing_how_often, 
						  we_use_work = we_use_work, do_we_distribute = do_we_distribute, did_we_host = did_we_host, third_party_host = third_party_host, if_modified = if_modified, 
						  use_generate_code = use_generate_code, form_gen_code = form_gen_code, how_hard_replace = how_hard_replace, obligation = obligation, additional_comments = additional_comments,
						  software_name = software_name, software_version = software_version, authorization = authorization, requested_by = requested_by)
	new_license.save()

	if approver_session != True:
		for admin in User.objects.all():
				if admin.approver_status == True:
					send_mail('New license request on OpenSource site', admin.username + ",\n    There is a new license request for software "+new_license.software_name+" version "+new_license.software_version+" on the Marketlive OpenSource site, requested by "+new_license.requested_by+". Please log in to accept or decline this request.",
							  'wolfa97@comcast.net', [admin.email], fail_silently = False)

	template  = loader.get_template('Base/request_sent.html') 
	context   = RequestContext(request, {
		'auth_session'   	: auth_session,
		'approver_session' 	: approver_session,

	})
	return HttpResponse(template.render(context))
	

def user_requests(request):
	if 'auth' in request.session:
		auth_session = request.session['auth']
	else:
		auth_session = False
	if 'approver' in request.session:
		approver_session = request.session['approver']
	else:
		approver_session = False

	if 'current_user' in request.session and auth_session == True:
		current_username = request.session['current_user']
		current_user = User.objects.get(username = current_username)
		current_user_approver_status = current_user.approver_status
	else:
		current_user_approver_status = False

	user_list = []
	for urequest in User_request.objects.all():
		if urequest.denied != True:
			a = 'user_'
			b = str(urequest.username)
			c = a+b
			c = [urequest.username, urequest.first_name, urequest.last_name]
			user_list.append(c)


	if current_user_approver_status == True:
		template  = loader.get_template('Base/user_requests.html') 
		context   = RequestContext(request, {
			'auth_session'   : auth_session,
			'user_list'      : user_list,
			'approver_session' 	: approver_session,
		})
		return HttpResponse(template.render(context))


	else:
		template  = loader.get_template('Base/not_approver.html')
		context   = RequestContext(request, {
			'auth_session'	   : auth_session,

		})
		return HttpResponse(template.render(context))

def user_request_detail(request, viewed_username):
	if 'auth' in request.session:
		auth_session = request.session['auth']
	else:
		auth_session = False
	if 'approver' in request.session:
		approver_session = request.session['approver']
	else:
		approver_session = False

	if 'current_user' in request.session and auth_session == True:
		current_username = request.session['current_user']
		current_user = User.objects.get(username = current_username)
		current_user_approver_status = current_user.approver_status
	else:
		current_user_approver_status = False

	viewed_user = User_request.objects.get(username = viewed_username)

	if current_user_approver_status == True:
		template  = loader.get_template('Base/user_request_details.html') 
		context   = RequestContext(request, {
			'auth_session' 			 : auth_session,
			'user_request_firstname' : viewed_user.first_name,
			'user_request_lastname'  : viewed_user.last_name,
			'user_request_username'	 : viewed_user.username,
			'user_request_email'	 : viewed_user.email,
			'user_request_password'  : viewed_user.password,
			'approver_session'		 : approver_session,
		})
		return HttpResponse(template.render(context))

	else:
		template  = loader.get_template('Base/not_approver.html')
		context   = RequestContext(request, {
			'auth_session' : auth_session,
		})
		return HttpResponse(template.render(context))



def user_approved(request):
	unaltered_username = request.POST['request_unalt_username']
	new_username       = request.POST['request_username']
	new_firstname      = request.POST['request_first_name']
	new_lastname       = request.POST['request_last_name']
	new_email          = request.POST['request_email']
	new_password       = request.POST['request_password']
	new_approverstatus_string = request.POST['request_approver_status']
	
	if new_approverstatus_string == 'True':
		new_approverstatus = True
	else:
		new_approverstatus = False


	if not new_username or not new_firstname or not new_lastname or not new_email or not new_password:
		return HttpResponseRedirect('/user_requests')
	else:
		new_user = User(username = new_username, first_name = new_firstname, last_name = new_lastname,
		email = new_email, password = new_password, approver_status = new_approverstatus)

	new_user.save()

	send_mail('User request on OpenSource website accepted', new_user.first_name +" "+ new_user.last_name + ",\n    " + 
			  "Your request to become an authorized user on the Marketlive OpenSource website was accepted. Username: "+
			  new_user.username+", Password: "+new_user.password+".", 'wolfa97@comcast.net', [new_user.email], fail_silently = False)

	old_request = User_request.objects.get(username = unaltered_username)
	old_request.delete()

	template = loader.get_template('Base/user_approved.html')
	context  = RequestContext(request, {
		'new_username' 		 : new_username,
		'new_firstname'		 : new_firstname,
		'new_lastname'		 : new_lastname,
		'new_email'			 : new_email,
		'new_approverstatus' : new_approverstatus,
	})
	return HttpResponse(template.render(context))



def user_denied(request):
	new_username = request.POST['request_username']
	denied_user = User_request.objects.get(username = new_username)
	denied_user.denied = True
	denied_user.save()

	template = loader.get_template('Base/user_denied.html')
	context = RequestContext(request, {
		'username' : denied_user.username,
	})
	return HttpResponse(template.render(context))