time_zone = 'UTC'				   	#the three letter code, for example "UTC" for Pacific.

company_name = 'Marketlive'		   	#your company's name.

from_email = 'wolfa97@comcast.net' 	#email address you want all emails from this website to come from. Full address!
email_host = 'smtp.comcast.net'    	#smtp.something.com/net, or smtp.everything_after_the_@_in_your_email (most likely)
email_username = 'wolfa97'		   	#what you would use to log onto this email account
email_password = 'Willy2006'	   	#what you would use to log onto this email account
email_port = 587				   	#optimal port varies per host. You may need to look it up online. (Probably 587)

#Put your company's logo into "Base/static/Base".
ilogo = 'ML_Logo.png'	 			#name of the image, with extention

site_url = 'localhost:8000'			#your site's url. The bit after the "www." or "http://", including the ".com" or whatever ending.
									#THIS DOES NOT SET IT UP ONLINE FOR YOU, IT IS SIMPLY TO LET DJANGO KNOW WHAT HOSTS TO ALLOW
debug = True						#turn off when website is up and running! Helps with errors, but is a security problem if left on.

#ignore this:
logo = "Base/"+ilogo