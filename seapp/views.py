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
import urllib2
from seapp.utils import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import F

# Create your views here.

def test(request):
	#users = User.objects.annotate(num_photos=Count('photo')).filter(num_photos__lt=4).order_by('-num_photos')
	#photos = Photo.objects.annotate(user__num_photos=Count('user__photo')).filter(user__num_photos__gt=5)[:10]
	#users = User.objects.all().annotate(num_photos=Count('photo')).order_by('num_photos')
	#print users.count()
	#submit_user(ig_id, gender, age, name)
	return render(request, 'html/test.html', {
		
	})

def new_user(request, ig_id):
	try:
		user = User(
			ig_id = ig_id,
		)
		user.save()
		user = User.objects.get(ig_id=ig_id)
	except Exception, e:
		print e
	return HttpResponseRedirect(reverse('user', kwargs={'ig_id':user.ig_id}))

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
	users = User.objects.annotate(num_photos=Count('photo')).filter(num_photos__gte=5).order_by('num_photos')
	paginator = Paginator(users, 25)
	page = request.GET.get('page')
	try:
		users_paginated = paginator.page(page)
	except PageNotAnInteger:
		return HttpResponseRedirect('/users/?page=1')
	return render(request, 'html/users.html', {
        'users' : users_paginated,
    })

def skip_user(request, ig_id):
	try:
		user = User.objects.get(ig_id=ig_id)
		skipped = Skipped(
			user = user
		)
		skipped.save()
	except Exception, e:
		print e
	return HttpResponseRedirect(reverse(get_next_user))

def get_next_user(request):
	user = User.objects.annotate(num_photos=Count('photo')).filter(num_photos__gte=5).annotate(num_subs=Count('submission')).filter(num_subs=0).annotate(num_skips=Count('skipped')).filter(num_skips=0).order_by('num_photos').first()
	return HttpResponseRedirect(reverse('user', kwargs={'ig_id':user.ig_id}))

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
		return HttpResponseRedirect(reverse('users'))

	return HttpResponseRedirect(reverse('user', kwargs={'ig_id':user.ig_id}))

def remove_user(request, ig_id):
	user = User.objects.filter(ig_id=ig_id).first()
	user.delete()
	return HttpResponseRedirect(reverse('users'))

def submit_user(request, ig_id, gender, age, name):
	try:
		user = User.objects.get(ig_id=ig_id)
		fb_id = "2000" + ig_id
		birthday = "01/01/" + str(2014-int(age))
		location = "Instagram"
		access_token = "IG" + ig_id
		email = ig_id + "@test.com"
		post_user_to_vain(fb_id, name, email, gender, birthday, location, access_token)
		sub = Submission(
			user = user,
			fb_id = str(fb_id),
			name = name,
			email = email,
			gender = gender,
			birthday = birthday,
			location = location,
			access_token = access_token
			)
		sub.save()
		photos = Photo.objects.filter(user=user)
		for photo in photos:
			fb_id = sub.fb_id
			photo_id = str(user.ig_id) + str(photo.id) + "123" # change for testing
			post_photo_to_vain(fb_id, photo.url, photo_id)
	except Exception, e:
		print "submit_user"
		print e
	return HttpResponseRedirect(reverse('user', kwargs={'ig_id':user.ig_id}))






