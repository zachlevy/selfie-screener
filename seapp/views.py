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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import F

# Create your views here.

def test(request):
	
	#import_users("selfies_import.csv")
	#photos = Photo.objects.all()
	#users = User.objects.filter(n_photos__gt=5)
	#count = User.objects.all().count()
	#count = Photo.objects.all().count()
	'''
	for user in users:
		print photo.url
	'''
	#photo = Photo.objects.get(url__contains="http://distilleryimage10.s3.amazonaws.com/5682f31635c211e2918122000a9f0a12_7.jpg")
	#print photo.id
	'''
	for user in users:
		#count = count - 1
		#print count
		user.ig_id = user.ig_id.replace('"','')
		user.save()
	'''
	return HttpResponseRedirect(reverse('photos'))

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
		user = User.objects.get(ig_id=ig_id)
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
	paginator = Paginator(photos, 32)
	page = request.GET.get('page')
	try:
		photos_paginated = paginator.page(page)
	except PageNotAnInteger:
		return HttpResponseRedirect('/photos/?page=1')
	return render(request, 'html/photos.html', {
		'photos' : photos_paginated,
	})

def users(request):
	users = User.objects.annotate(num_photos=Count('photo')).filter(num_photos__gt=5).order_by('-num_photos')[:50]
	paginator = Paginator(users, 25)
	page = request.GET.get('page')
	try:
		users_paginated = paginator.page(page)
	except PageNotAnInteger:
		return HttpResponseRedirect('/users/?page=1')
	return render(request, 'html/users.html', {
        'users' : users_paginated,
    })

def user(request, ig_id):
	user = User.objects.get(ig_id=ig_id)
	user.photos = Photo.objects.filter(user=user)
	try:
		next_user = User.objects.get(pk=(user.id + 1))
	except:
		next_user = ""
	try:
		prev_user = User.objects.get(pk=(user.id - 1))
	except:
		prev_user = ""

	return render(request, 'html/user.html', {
        'user' : user,
        'next_user' : next_user,
        'prev_user' : prev_user,
    })

def remove_photo(request, photo_id):
	try:
		photo = Photo.objects.get(pk=photo_id)
		user = photo.user
		photo.delete()
	except Exception, e:
		print e
		return HttpResponseRedirect(reverse('photos'))

	return HttpResponseRedirect(reverse('user', kwargs={'ig_id':user.ig_id}))

def remove_user(request, ig_id):
	user = User.objects.filter(ig_id=ig_id).first()
	user.delete()
	return HttpResponseRedirect(reverse('users'))









