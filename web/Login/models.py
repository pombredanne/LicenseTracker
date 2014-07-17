from django.db import models

class User(models.Model):
	username = models.CharField(max_length = 100)
	password = models.CharField(max_length = 100)
	first_name = models.CharField(max_length = 25)
	last_name = models.CharField(max_length = 50)
	approver_status = models.NullBooleanField()
	email = models.EmailField()

	def __str__(self):
		return self.username


class User_request(models.Model):
	username = models.CharField(max_length = 100)
	password = models.CharField(max_length = 100)
	first_name = models.CharField(max_length = 25)
	last_name = models.CharField(max_length = 50)
	email = models.EmailField()
	denied = models.NullBooleanField()

	def __str__(self):
		return self.username

	#more and stuff!


# Create your models here.
