from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from Login.models import User, User_request, Pass_reset
from django.core.mail import send_mail

def login(request):
	if 'auth' in request.session:
		auth_session = request.session['auth']
	else:
		auth_session = False
	template  = loader.get_template('Login/index.html') 
	context   = RequestContext(request, {
		'auth_session': auth_session,
	})

	return HttpResponse(template.render(context))

def testo(request):
	userlist = []
	unauthorized_userlist = []
	for usr in User.objects.all():
		userlist.append(usr.username)
	for unauthusr in User_request.objects.all():
		unauthorized_userlist.append(unauthusr.username)
	request.session.set_expiry(0)

	entered_name     = request.POST['typed_username']
	entered_password = request.POST['typed_password']

	if entered_name in userlist:
		active_user = User.objects.get(username = entered_name)
		if active_user.password == entered_password:
			request.session['auth'] = True
			request.session['current_user'] = active_user.username
			template = loader.get_template('Login/login_success.html')
			request.session['approver'] = active_user.approver_status
		else:
			request.session['auth'] = False
			template = loader.get_template('Login/login_failed.html')
	
	elif entered_name in unauthorized_userlist:
		active_user = User_request.objects.get(username = entered_name)
		if active_user.password == entered_password:
			request.session['auth'] = False
			template = loader.get_template('Login/user_unauthorized.html')

			context = RequestContext(request, {
				'denied' : active_user.denied,
			})
			return HttpResponse(template.render(context))

		else:
			request.session['auth'] = False
			template = loader.get_template('Login/login_failed.html')

	else:	
		request.session['auth'] = False
		template = loader.get_template('Login/login_failed.html')
		

	context = RequestContext(request, {
		'entered_name' : entered_name,
		'userlist'     : userlist,


	})
	return HttpResponse(template.render(context))
	
def new_user(request):
	if 'error' in request.session:
		error_message = request.session['error']
		del request.session['error']
	else: 
		error_message = False
	template  = loader.get_template('Login/new_user.html') 
	context   = RequestContext(request, {
		'error_message' : error_message,
	})
	return HttpResponse(template.render(context))

def request_sent(request):
	requested_username = request.POST['requested_username']
	requested_password = request.POST['requested_password']
	confirm_password   = request.POST['confirm_password']
	request_first_name = request.POST['request_first_name']
	request_last_name  = request.POST['request_last_name']
	request_email      = request.POST['request_email']

	userlist = []
	unauthorized_userlist = []
	for usr in User.objects.all():
		userlist.append(usr.username)
	for unauthusr in User_request.objects.all():
		unauthorized_userlist.append(unauthusr.username)

	if requested_username in userlist or requested_username in unauthorized_userlist:
		request.session['error'] = 'Username already taken.'
		return HttpResponseRedirect('/login/new_user')
		

	elif not requested_username or not requested_password or not confirm_password or not request_first_name or not request_last_name or not request_email:
		request.session['error'] = 'One or more fields was left blank.'
		return HttpResponseRedirect('/login/new_user')

	elif requested_password != confirm_password:
		request.session['error'] = 'Passwords did not match.'
		return HttpResponseRedirect('/login/new_user')

	else:
		new_user_request = User_request(username = requested_username, password = requested_password, first_name = request_first_name, last_name = request_last_name, email = request_email)
		new_user_request.save()
		approver_email_list = []
		for admin in User.objects.all():
			if admin.approver_status == True:
				send_mail('New user request on OpenSource site', admin.username + ",\n    " + new_user_request.first_name+" "+new_user_request.last_name+" has sent a request to become an authorized user on the Marketlive OpenSource database website. Please log on to accept or reject this request.", 'wolfa97@comcast.net', [admin.email], fail_silently = False)

	auth_test = request.session['auth']

	template = loader.get_template('Login/request_sent.html')
	context  = RequestContext(request, {
		'requested_username': requested_username,
		'request_first_name': request_first_name,
		'request_last_name' : request_last_name,
		'auth_test'         : auth_test,
	})
	return HttpResponse(template.render(context))

def logout(request):
	request.session['current_user'] = False
	request.session['auth']         = False
	request.session['approver']		= False
	return HttpResponseRedirect('/login')

def forgot_password(request):
	if 'forgot_error' in request.session:
		error_message = request.session['forgot_error']
		del request.session['forgot_error']
	else: 
		error_message = False
	template  = loader.get_template('Login/forgot_password.html') 
	context   = RequestContext(request, {
		'error': error_message,
	})
	return HttpResponse(template.render(context))

def password_request_sent(request):
	username = request.POST['username']
	comments = request.POST['comments']

	if not comments or comments == 'Any comments?':
		comments = 'No comments'

	userlist = []
	for usr in User.objects.all():
		userlist.append(usr.username)

	if username in userlist:
		a = User.objects.get(username = username)
		b = Pass_reset(user = a, text = comments)
		b.save()
		template  = loader.get_template('Login/password_request_sent.html') 
		context   = RequestContext(request, {
			'user': b,
		})
		return HttpResponse(template.render(context))

	elif not username:
		request.session['forgot_error'] = 'You did not type in a username'
		return HttpResponseRedirect('/login/forgot_password')
	else:
		request.session['forgot_error'] = 'There are no users with that username'
		return HttpResponseRedirect('/login/forgot_password')