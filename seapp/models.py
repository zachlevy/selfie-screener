from django.db import models

# Create your models here.

class User(models.Model):
	ig_id = models.CharField(max_length=1000)

	def __unicode__(self):  # Python 3: def __str__(self):
		return self.ig_id

class Photo(models.Model):
	user = models.ForeignKey(User)
	url = models.CharField(max_length=10000)

	def __unicode__(self):  # Python 3: def __str__(self):
		return self.url

