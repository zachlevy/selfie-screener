from seapp.models import *
from django.db.models import Count
from django.conf import settings
import csv
import urllib2
import urllib

def post_user_to_vain(fb_id, name, email, gender, birthday, location, access_token):
	try:
		#url = "http://localhost:8001/api/login_fb_user/"
		print url
		data = urllib.urlencode({
			"fb_id" : str(fb_id),
			"name" : name,
			"email" : email,
			"gender" : gender,
			"birthday" : birthday,
			"location" : location,
			"access_token" : access_token
			})
		content = urllib2.urlopen(url=url, data=data).read()
	except Exception, e:
		print "post_user_to_vain"
		print e

def post_photo_to_vain(fb_id, photo_url, photo_id):
	try:
		#url = "http://localhost:8001/api/upload_photo_aws/"
		data = urllib.urlencode({
			"fb_id" : str(fb_id),
			"photo_url" : photo_url,
			"photo_id" : str(photo_id)
			})
		print url
		content = urllib2.urlopen(url=url, data=data).read()
	except Exception, e:
		print "post_photo_to_vain"
		print e

def import_users(file_location):
	print "import_users"
	with open(file_location, 'rU') as csvfile:
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

def delete_singles(limit):
	#user_count = User.objects.annotate(num_photos=Count('photo')).exclude(num_photos__gte=limit).order_by('-num_photos').count()
	#print user_count
	#users = User.objects.annotate(num_photos=Count('photo')).exclude(num_photos__gte=limit).order_by('-num_photos')
	print Photo.objects.all().count()
	print User.objects.all().count()

class BreakIt(Exception): pass

def check_photos(users):
	for user in users:
		print "checking user" + str(user.ig_id)
		photos = Photo.objects.filter(user=user)
		for photo in photos:
			req = urllib2.Request(photo.url)
			try:
				print "checking photo"
				resp = urllib2.urlopen(req)
			except urllib2.URLError, e:
			    if e.code == 404:
			    	print "404 brah"
			    	photos = Photo.objects.filter(user=user)
			    	if photos.count() <= 4:
			    		print "delete user"
			    		user.delete()
			    		break
			    	else:
			    		print "delete photo"
			    		photo.delete()
			    else:
			    	print "error not 404 brah"
			    	photos = Photo.objects.filter(user=user)
			    	if photos.count() <= 4:
			    		print "delete user"
			    		user.delete()
			    		break
			    	else:
			    		print "delete photo"
			    		photo.delete()




