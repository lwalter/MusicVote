from django import forms
from django.contrib.auth.models import User
from MusicVoteApp.models import MusicChannel, MusicChannelSong

class UserForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class CreateChannelForm(forms.ModelForm):
    channel_name = forms.CharField(widget = forms.TextInput())
    class Meta:
        model = MusicChannel
        #exclude = ('slug',)
        fields = ('channel_name',)

class AddChannelSongForm(forms.ModelForm):
    song_url = forms.CharField(widget = forms.TextInput())

    class Meta:
        model = MusicChannelSong
        fields = ('song_url',)
