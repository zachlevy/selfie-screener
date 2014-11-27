from seapp.models import *
from django.db.models import Count
from django.conf import settings
import csv

def import_users(file_location):
	print "import_users"
	with open(file_location, 'rU') as csvfile:
		#selfies = csv.reader(csvfile, delimiter=',', quotechar='"')
		selfies = csv.reader(csvfile)
		for row in selfies:
			ig_id = row[1]
			url = row[0]
			try:
				user = User.objects.get(ig_id=ig_id)
			except:
				user = User(
					ig_id = ig_id
					)
				user.save()
				user = User.objects.get(ig_id=ig_id)
			try:
				photo = Photo(
					user = user,
					url = url
					)
				photo.save()
			except Exception, e:
				print e