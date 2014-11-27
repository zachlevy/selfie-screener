from django.conf.urls import patterns, include, url
import seapp.views
from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'selfies.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^photos/$', seapp.views.photos, name="photos"),
    url(r'^new-photo/(?P<ig_id>.*)/(?P<url>.*)/$', seapp.views.new_photo, name="new_photo"),
    url(r'^remove-photo/(?P<id>.*)/$', seapp.views.remove_photo, name="remove_photo"),
    url(r'^users/$', seapp.views.users, name="users"),
    url(r'^user/(?P<ig_id>.*)/$', seapp.views.user, name="user"),
    url(r'^new-user/(?P<ig_id>.*)/$', seapp.views.new_user, name="new_user"),
    url(r'^remove-user/(?P<ig_id>.*)/$', seapp.views.remove_user, name="remove_user"),
    url(r'^admin/', include(admin.site.urls)),
)