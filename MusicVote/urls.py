from django.conf.urls import patterns, include, url
from django.contrib import admin
from MusicVoteApp import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^home/$', views.home, name='home'),
    url(r'^musicchannel/(?P<music_channel_slug>[\w\-]+)/$', views.music_channel, name='musicchannel'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^vote/$', views.vote, name='vote'),
    url(r'^get_next_song/$', views.get_next_song, name='get_next_song'),
    url(r'^send_message/$', views.send_message, name='send_message'),
    url(r'^admin/', include(admin.site.urls)),
)