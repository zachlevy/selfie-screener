from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from seapp.models import *
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.conf import settings
import urllib
from seapp.utils import *

# Create your views here.

def new_user(request, ig_id):
	try:
		user = User(
			ig_id = ig_id,
		)
		user.save()
		user = User.objects.get(ig_id=ig_id)
	except Exception, e:
		print e
	return HttpResponseRedirect(reverse('user', kawrgs={'ig_id':user.ig_id}))

def new_photo(request, ig_id, url):
	try:
		print ig_id
		print url
		user = User.objects.get(ig_id=ig_id)
		print user
		photo = Photo(
			user = user,
			url = "https://i.imgur.com/9Zx0eij.jpg",
			)
		photo.save()
	except Exception, e:
		print e
	return HttpResponseRedirect(reverse('photos'))

def photos(request):
	photos = Photo.objects.all()
	print photos
	return render(request, 'html/photos.html', {
        'photos' : photos,
    })

def users(request):
	users = User.objects.all()
	return render(request, 'html/users.html', {
        'users' : users,
    })

def user(request, ig_id):
	user = User.objects.get(ig_id=ig_id)
	user.photos = Photo.objects.filter(user=user)
	return render(request, 'html/user.html', {
        'user' : user,
    })

def remove_photo(request, photo_id):
	photo = Photo.objects.get(pk=photo_id)
	user = photo.user
	photo.remove()
	return HttpResponseRedirect(reverse('user', kawrgs={'ig_id':user.ig_id}))

def remove_user(request, ig_id):
	user = User.objects.filter(ig_id=ig_id).first()
	user.delete()
	return HttpResponseRedirect(reverse('users'))









