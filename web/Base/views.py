from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from Login.models import User, User_request
from django.core.mail import send_mail
from Base.models import License
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
	
def view_licenses(request, pagenum):
	if 'auth' in request.session:
		auth_session = request.session['auth']
	else:
		auth_session = False
	if 'approver' in request.session:
		approver_session = request.session['approver']
	else:
		approver_session = False

	license_list = []
	for license in License.objects.extra( select={'lower_name':'lower(software_name)'}).order_by('lower_name'):
		if license.authorization == "accepted" or license.authorization == 'denied':
			a = '_license'
			b = str(license.software_name)
			c = b+a
			c = [license.software_name[:20], license.software_version[:12], license.license_type[:15], license.date_requested, license.id, license.authorization]
			license_list.append(c)

	p = Paginator(license_list, 20)
	try:
		current_page = p.page(pagenum)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		current_page = p.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		current_page = p.page(p.num_pages)

	template  = loader.get_template('Base/view_licenses.html') 
	context   = RequestContext(request, {
		'auth_session' 		: auth_session,
		'approver_session' 	: approver_session,
		'license_list'		: current_page.object_list,
		'current_page'		: current_page,
	})
	return HttpResponse(template.render(context))

def view_licenses_search(request):
	query = request.GET.get('search', '')
	word_list = query.split()
	name_list = []
	for license in License.objects.all():
		if license.authorization == 'accepted' or license.authorization == 'denied':
			name_list.append(license.software_name)
			name_list.append(license.license_type)
			name_list.append(license.requested_by)


	successful = []
	for name in name_list:
		if name.lower() in (word.lower() for word in word_list):			
			successful.append(name)

	successful_user = []
	for match in successful:
		a = License.objects.filter(software_name = match)
		b = License.objects.filter(license_type = match)
		c = License.objects.filter(requested_by = match)
		for d in a:	
			if not d in successful_user: 
				successful_user.append(d)
		for d in b:	
			if not d in successful_user: 
				successful_user.append(d)
		for d in c:	
			if not d in successful_user: 
				successful_user.append(d)

	return HttpResponse(successful_user)

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
					try:
						send_mail('New license request on OpenSource site', admin.username + ",\n    There is a new license request for software "+new_license.software_name+" version "+new_license.software_version+" on the Marketlive OpenSource site, requested by "+new_license.requested_by+". Please log in to accept or decline this request.",
							  'wolfa97@comcast.net', [admin.email], fail_silently = False)
					except SMTPRecipientsRefused:
						pass

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

	user_list = []
	for urequest in User_request.objects.all():
		if urequest.denied != True:
			a = 'user_'
			b = str(urequest.username)
			c = a+b
			c = [urequest.username, urequest.first_name, urequest.last_name]
			user_list.append(c)


	if approver_session == True:
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

	viewed_user = User_request.objects.get(username = viewed_username)

	if approver_session == True:
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

	try:
		send_mail('User request on OpenSource website accepted', new_user.first_name +" "+ new_user.last_name + ",\n    " + 
			  "Your request to become an authorized user on the Marketlive OpenSource website was accepted. Username: "+
			  new_user.username+", Password: "+new_user.password+".", 'wolfa97@comcast.net', [new_user.email], fail_silently = False)
	except SMTPRecipientsRefused:
		pass

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

def license_requests(request):
	if 'auth' in request.session:
		auth_session = request.session['auth']
	else:
		auth_session = False
	if 'approver' in request.session:
		approver_session = request.session['approver']
	else:
		approver_session = False
	
	license_list = []
	for lrequest in License.objects.all():
		if lrequest.authorization == 'none' or not lrequest.authorization:
			a = '_license'
			b = str(lrequest.software_name)
			c = b+a
			c = [lrequest.software_name[:20], lrequest.software_version[:12], lrequest.license_type[:15], lrequest.date_requested, lrequest.id]
			license_list.append(c)

	if auth_session == True:
		template  = loader.get_template('Base/license_requests.html') 
		context   = RequestContext(request, {
			'auth_session' 		: auth_session,
			'approver_session' 	: approver_session,
			'license_list'		: license_list,
		})
		return HttpResponse(template.render(context))
	else:
		return HttpResponseRedirect('/login')

def request_detail(request, license_id):
	if 'auth' in request.session:
		auth_session = request.session['auth']
	else:
		auth_session = False
	if 'approver' in request.session:
		approver_session = request.session['approver']
	else:
		approver_session = False

	viewed_license = License.objects.get(id = license_id)

	if approver_session == True:
		template  = loader.get_template('Base/license_request_details.html') 
		context   = RequestContext(request, {
			'auth_session' 		  : auth_session,
			'approver_session'	  : approver_session,
			'software_name'		  : viewed_license.software_name,
			'software_version'	  : viewed_license.software_version,
			'licensor_name'		  : viewed_license.licensor_name,
			'license_type'		  : viewed_license.license_type,
			'copy_of_license'	  : viewed_license.copy_of_license,
			'where_used'		  : viewed_license.where_used,
			'client_where_used'	  : viewed_license.client_where_used,
			'desc_nature_work'	  : viewed_license.desc_nature_work,
			'desc_function_work'  : viewed_license.desc_function_work,
			'category_of_work'	  : viewed_license.category_of_work,
			'if_ML_paid_for'	  : viewed_license.if_ML_paid_for,
			'ML_pay_twenfivk'	  : viewed_license.ML_pay_twenfivk,
			'ongoing_payments'	  : viewed_license.ongoing_payments,
			'ongoing_how_much'	  : viewed_license.ongoing_how_much,
			'ongoing_how_often'	  : viewed_license.ongoing_how_often,
			'we_use_work'		  : viewed_license.we_use_work,
			'do_we_distribute'	  : viewed_license.do_we_distribute,
			'did_we_host'		  : viewed_license.did_we_host,
			'third_party_host'	  : viewed_license.third_party_host,
			'if_modified'		  : viewed_license.if_modified,
			'use_generate_code'	  : viewed_license.use_generate_code,
			'form_gen_code'		  : viewed_license.form_gen_code,
			'how_hard_replace'	  : viewed_license.how_hard_replace,
			'obligation'		  : viewed_license.obligation,
			'additional_comments' : viewed_license.additional_comments,
			'requested_by'		  : viewed_license.requested_by,
			'authorization'		  : viewed_license.authorization,
			'date_requested'	  : viewed_license.date_requested,
			'license_id'		  : viewed_license.id,
		})
		return HttpResponse(template.render(context))

	else:
		template  = loader.get_template('Base/not_approver.html')
		context   = RequestContext(request, {
			'auth_session' : auth_session,
		})
		return HttpResponse(template.render(context))

def license_approved(request):
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
	if use_generate_code:
		form_gen_code 		= request.POST['form_gen_code']
	how_hard_replace 	= request.POST['how_hard_replace']
	obligation 			= request.POST.get('obligation', False)
	additional_comments = request.POST['additional_comments']
	software_name 		= request.POST['software_name']
	software_version 	= request.POST['software_version']
	license_id			= request.POST['license_id']

	if not ongoing_payments:	
		ongoing_how_much = 0
		ongoing_how_often = 0

	if not use_generate_code:
		form_gen_code = 'Not Used to Generate Code'

	if not licensor_name or not license_type or not copy_of_license or not where_used or not client_where_used or not desc_nature_work or not desc_function_work or not category_of_work or not do_we_distribute or not form_gen_code or not how_hard_replace or not additional_comments or not software_name or not software_version:
		return HttpResponse("One or more fields was left blank. Please press your browser's 'back' button and check all boxes.")

	approved_license = License.objects.get(id = license_id)

	approved_license.licensor_name = licensor_name
	approved_license.license_type = license_type
	approved_license.copy_of_license = copy_of_license
	approved_license.where_used = where_used
	approved_license.client_where_used = client_where_used
	approved_license.desc_nature_work = desc_nature_work
	approved_license.desc_function_work = desc_function_work
	approved_license.category_of_work = category_of_work
	approved_license.if_ML_paid_for = if_ML_paid_for
	approved_license.ML_pay_twenfivk = ML_pay_twenfivk
	approved_license.ongoing_payments = ongoing_payments
	approved_license.ongoing_how_much = ongoing_how_much
	approved_license.ongoing_how_often = ongoing_how_often
	approved_license.we_use_work = we_use_work
	approved_license.do_we_distribute = do_we_distribute
	approved_license.did_we_host = did_we_host
	approved_license.third_party_host = third_party_host
	approved_license.if_modified = if_modified
	approved_license.use_generate_code = use_generate_code
	approved_license.form_gen_code = form_gen_code
	approved_license.how_hard_replace = how_hard_replace
	approved_license.obligation = obligation
	approved_license.additional_comments = additional_comments
	approved_license.software_name = software_name
	approved_license.software_version = software_version
	approved_license.authorization = 'accepted'
	approved_license.save()

	template  = loader.get_template('Base/license_approved.html') 
	context   = RequestContext(request, {
		'auth_session'   	: auth_session,
		'approver_session' 	: approver_session,
	})
	return HttpResponse(template.render(context))

def license_denied(request):
	if 'auth' in request.session:
		auth_session = request.session['auth']
	else:
		auth_session = False
	if 'approver' in request.session:
		approver_session = request.session['approver']
	else:
		approver_session = False

	license_id = request.POST['license_id']
	denied_license = License.objects.get(id = license_id)
	denied_license.authorization = 'denied'
	denied_license.save()
	template  = loader.get_template('Base/license_denied.html') 
	context   = RequestContext(request, {
		'auth_session'   	: auth_session,
		'approver_session' 	: approver_session,
	})
	return HttpResponse(template.render(context))

def license_detail(request, license_id):
	if 'auth' in request.session:
		auth_session = request.session['auth']
	else:
		auth_session = False
	if 'approver' in request.session:
		approver_session = request.session['approver']
	else:
		approver_session = False
	
	license = License.objects.get(id = license_id)

	if auth_session == True:
		template  = loader.get_template('Base/license_detail.html') 
		context   = RequestContext(request, {
			'auth_session' 		  : auth_session,
			'approver_session'	  : approver_session,
			'software_name'		  : license.software_name,
			'software_version'	  : license.software_version,
			'licensor_name'		  : license.licensor_name,
			'license_type'		  : license.license_type,
			'copy_of_license'	  : license.copy_of_license,
			'where_used'		  : license.where_used,
			'client_where_used'	  : license.client_where_used,
			'desc_nature_work'	  : license.desc_nature_work,
			'desc_function_work'  : license.desc_function_work,
			'category_of_work'	  : license.category_of_work,
			'if_ML_paid_for'	  : license.if_ML_paid_for,
			'ML_pay_twenfivk'	  : license.ML_pay_twenfivk,
			'ongoing_payments'	  : license.ongoing_payments,
			'ongoing_how_much'	  : license.ongoing_how_much,
			'ongoing_how_often'	  : license.ongoing_how_often,
			'we_use_work'		  : license.we_use_work,
			'do_we_distribute'	  : license.do_we_distribute,
			'did_we_host'		  : license.did_we_host,
			'third_party_host'	  : license.third_party_host,
			'if_modified'		  : license.if_modified,
			'use_generate_code'	  : license.use_generate_code,
			'form_gen_code'		  : license.form_gen_code,
			'how_hard_replace'	  : license.how_hard_replace,
			'obligation'		  : license.obligation,
			'additional_comments' : license.additional_comments,
			'requested_by'		  : license.requested_by,
			'authorization'		  : license.authorization,
			'date_requested'	  : license.date_requested,
			'license_id'		  : license.id,
		})
		return HttpResponse(template.render(context))
	else:
		return HttpResponseRedirect('/login')

def license_changed(request):
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
	if use_generate_code:
		form_gen_code 		= request.POST['form_gen_code']
	how_hard_replace 	= request.POST['how_hard_replace']
	obligation 			= request.POST.get('obligation', False)
	additional_comments = request.POST['additional_comments']
	software_name 		= request.POST['software_name']
	software_version 	= request.POST['software_version']
	license_id			= request.POST['license_id']
	authorization		= request.POST['authorization']

	if not ongoing_payments:	
		ongoing_how_much = 0
		ongoing_how_often = 0

	if not use_generate_code:
		form_gen_code = 'Not Used to Generate Code'

	if not licensor_name or not license_type or not copy_of_license or not where_used or not client_where_used or not desc_nature_work or not desc_function_work or not category_of_work or not do_we_distribute or not form_gen_code or not how_hard_replace or not additional_comments or not software_name or not software_version:
		return HttpResponse("One or more fields was left blank. Please press your browser's 'back' button and check all boxes.")

	altered_license = License.objects.get(id = license_id)

	altered_license.licensor_name 		= licensor_name
	altered_license.license_type 		= license_type
	altered_license.copy_of_license 	= copy_of_license
	altered_license.where_used 			= where_used
	altered_license.client_where_used 	= client_where_used
	altered_license.desc_nature_work 	= desc_nature_work
	altered_license.desc_function_work 	= desc_function_work
	altered_license.category_of_work 	= category_of_work
	altered_license.if_ML_paid_for 		= if_ML_paid_for
	altered_license.ML_pay_twenfivk 	= ML_pay_twenfivk
	altered_license.ongoing_payments 	= ongoing_payments
	altered_license.ongoing_how_much 	= ongoing_how_much
	altered_license.ongoing_how_often 	= ongoing_how_often
	altered_license.we_use_work 		= we_use_work
	altered_license.do_we_distribute 	= do_we_distribute
	altered_license.did_we_host 		= did_we_host
	altered_license.third_party_host 	= third_party_host
	altered_license.if_modified 		= if_modified
	altered_license.use_generate_code	= use_generate_code
	altered_license.form_gen_code 		= form_gen_code
	altered_license.how_hard_replace 	= how_hard_replace
	altered_license.obligation 			= obligation
	altered_license.additional_comments = additional_comments
	altered_license.software_name 		= software_name
	altered_license.software_version 	= software_version
	altered_license.authorization 		= authorization
	altered_license.save()

	template  = loader.get_template('Base/license_changed.html') 
	context   = RequestContext(request, {
		'auth_session'   	: auth_session,
		'approver_session' 	: approver_session,
	})
	return HttpResponse(template.render(context))

#def template_view(request):
	#if 'auth' in request.session:
	#	auth_session = request.session['auth']
	#else:
	#	auth_session = False
	#if 'approver' in request.session:
	#	approver_session = request.session['approver']
	#else:
	#	approver_session = False
	#
	#VIEW
	#
	#if auth_session == True:
	#	template  = loader.get_template('Base/TEMPLATE.html') 
	#	context   = RequestContext(request, {
	#		'auth_session' 		: auth_session,
	#		'approver_session' 	: approver_session,
	#	})
	#	return HttpResponse(template.render(context))
	#else:
	#	return HttpResponseRedirect('/login')