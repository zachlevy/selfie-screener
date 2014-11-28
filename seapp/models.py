from django.db import models

# Create your models here.

class User(models.Model):
	ig_id = models.CharField(max_length=1000)

	def __unicode__(self):
		return self.ig_id

class Photo(models.Model):
	user = models.ForeignKey(User)
	url = models.CharField(max_length=10000)

	def __unicode__(self):
		return self.url

class Submission(models.Model):
	user = models.ForeignKey(User)
	fb_id = models.CharField(max_length=1000)
	gender = models.CharField(max_length=1000)
	birthday = models.CharField(max_length=1000)
	location = models.CharField(max_length=1000)
	access_token = models.CharField(max_length=1000)
	name = models.CharField(max_length=1000)
	email = models.CharField(max_length=1000)

	def __unicode__(self):
		return self.fb_id

class Skipped(models.Model):
	user = models.ForeignKey(User)

	def __unicode__(self):
		return self.user.ig_id
