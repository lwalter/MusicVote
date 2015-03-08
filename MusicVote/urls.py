from django.conf.urls import patterns, include, url
from django.contrib import admin
from MusicVoteApp import views

urlpatterns = patterns('',
    url(r'^$', views.index, name = 'index'),
    url(r'^register/$', views.register, name = 'register'),
    url(r'^login/$', views.login_user, name = 'login'),
    url(r'^home/$', views.home, name = 'home'),
    url(r'^musicchannel/(?P<music_channel_slug>[\w\-]+)/$', views.music_channel, name = 'musicchannel'),
    url(r'^logout_user/$', views.logout_user, name = 'logout_user'),
    url(r'^admin/', include(admin.site.urls)),
)
