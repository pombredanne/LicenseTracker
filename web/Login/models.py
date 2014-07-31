from django.db import models

class User(models.Model):
	username 		= models.CharField(max_length = 100)
	password 		= models.CharField(max_length = 200)
	first_name 		= models.CharField(max_length = 25)
	last_name 		= models.CharField(max_length = 50)
	approver_status = models.NullBooleanField()
	email 			= models.EmailField()
	password_reset	= models.NullBooleanField()

	def __str__(self):
		return self.username


class User_request(models.Model):
	username 	= models.CharField(max_length = 100)
	password 	= models.CharField(max_length = 100)
	first_name 	= models.CharField(max_length = 25)
	last_name 	= models.CharField(max_length = 50)
	email 		= models.EmailField()
	denied 		= models.NullBooleanField()

	def __str__(self):
		return self.username

class Pass_reset(models.Model):
	user 		= models.ForeignKey(User)
	text 		= models.TextField()
	date_sent 	= models.DateField(auto_now_add = True)

	#more and stuff!


# Create your models here.
