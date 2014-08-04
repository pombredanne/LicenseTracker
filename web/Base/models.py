from django.db import models
from Login.models import User

class License(models.Model):
	software_name 		= models.CharField(max_length = 50)		#name of program that needs its license accepted
	software_version 	= models.CharField(max_length = 20)    	#version of above software
	licensor_name 		= models.CharField(max_length = 50)		#No idea.
	license_type 		= models.CharField(max_length = 50)		#MIT, GNU Public, etc.
	copy_of_license 	= models.TextField()					#duh
	where_used 			= models.CharField(max_length = 100) 	#name and version of the component where this work will be used. Admin, B2C, CCOM, etc.
	client_where_used 	= models.CharField(max_length = 100)  	#include text about being "none"/"all"
	desc_nature_work 	= models.CharField(max_length = 200)	#brief desc of nature of work. Ex: source code, object code, documentation
	desc_function_work 	= models.CharField(max_length = 200)	#brief desc of function of work. 
	
	category_of_work_choices = (
		('none'			  , 'N/A'						 ),
		('app_web'		  , 'Application/Web Servers'	 ),
		('business_app'	  , 'Business Applications '	 ),
		('collab_commun'  , 'Collaboration/Communication'),
		('data_management', 'Data Management/Interaction'), 
		('database'		  , 'Database'					 ), 
		('design'		  , 'Design'					 ), 
		('dev_tools'	  , 'Development Tools'			 ), 
		('doc_content'	  , 'Document/Content Management'), 
		('lang_frameworks', 'Languages/Frameworks'		 ), 
		('networking'	  , 'Networking'				 ), 
		('op_systems'	  , 'Operating Systems/Tools'	 ), 
		('performance'	  , 'Performance/Scalability'	 ), 
		('proj_management', 'Project Management'		 ), 
		('security'		  , 'Security'					 ), 
		('testing'		  , 'Testing & Diagnostics'		 ), 
		('user_int'		  , 'User Interface'			 ), 
		('utility_other'  , 'Utility/Other'				 ), 
		('web_tools'	  , 'Web Tools'					 ),
	)

	category_of_work 	= models.CharField(max_length = 20, choices = category_of_work_choices, default = 'none')
	
	if_paid_for 		= models.NullBooleanField()				#somehow link with next 4
	pay_twenfivk 		= models.NullBooleanField()				#get only to show up if last is True
	ongoing_payments 	= models.NullBooleanField()				#ditto^
	ongoing_how_much	= models.IntegerField()				#only if if_paid_for and ongoing_payments both True 
	ongoing_how_often 	= models.IntegerField()				#label in weeks, months, whatevs. And ditto^
	we_use_work 		= models.NullBooleanField()				#do we use the 3rd party work, such as for internal use? Prob yes...

	do_we_distribute_choices = (
		('none'			, 'not distributed'				  ),
		('binary'		, 'binary distribution only'	  ),
		('source'		, 'source distribution only'	  ),
		('source_binary', 'source and binary distribution'),
		('script'		, 'script distribution'			  ),
		('image_icon'	, 'image / icon distribution'	  ),
		('mark-up'		, 'mark-up languages distribution'),
	)

	do_we_distribute 	= models.CharField(max_length = 14, choices = do_we_distribute_choices, default = 'none')

	did_we_host 		= models.NullBooleanField()				#including as embedded in a larger work or standalone
	third_party_host	= models.NullBooleanField()				#do we permit any third party to host the third party work?
	if_modified			= models.NullBooleanField()				#have we modified it in any manner?
	use_generate_code	= models.NullBooleanField()				#do we use 3rd party work to generate code or other material?

	form_gen_code		= models.CharField(max_length = 14, choices = do_we_distribute_choices, default = 'none')

	difficulty_choices	= (
		('trivial'			, 'trivial'			 ),
		('medium'			, 'medium'			 ),
		('hard'				, 'hard'			 ),
		('nearly_impossible', 'nearly_impossible'),
	)

	how_hard_replace	= models.CharField(max_length = 18, choices = difficulty_choices)

	obligation			= models.NullBooleanField()				#required to meet any obligation?
	additional_comments = models.TextField()
	
	date_requested		= models.DateField(auto_now_add = True)	#date requested. Sets itself at creation of this object.
	authorization		= models.CharField(max_length = 20)		#none/"none", "denied", "accepted"
	requested_by		= models.CharField(max_length = 100)	#is firstname lastname
	deny_reason			= models.TextField()

	def __str__(self):
		return self.software_name
