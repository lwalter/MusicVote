from django.shortcuts import render
from MusicVoteApp.forms import UserForm, CreateChannelForm, AddChannelSongForm
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth import authenticate, login
from datetime import datetime
from MusicVoteApp.models import MusicChannel, MusicChannelSong
from django.core.urlresolvers import reverse

def index(request):
	return render(request, 'MusicVoteApp/index.html')

def register(request):
	# Set registered flag to false initially
	registered = False

	# If its an HTTP POST, lets process the forms data
	if (request.method == 'POST'):
		form = UserForm(data = request.POST)

		# If the form is valid...
		if (form.is_valid()):
			# Save the users form to the database
			user = form.save()

			user.set_password(user.password)
			user.save()

			registered = True
		
		# Something went wrong
		else:
			print(form.errors)

	# Its not an HTTP POST, so lets just render a blank form
	else:
		form = UserForm()

	return render(
				request, 
				'MusicVoteApp/register.html', 
				{'form': form, 'registered': registered})

def login_user(request):
	if (request.method == 'POST'):
		# Get the users info and attempt to login
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username = username, password = password)

		if (user):
			# User provided valid credentials
			login(request, user)

			# Always return an HttpResponseRedirect after successfully dealing
			# with POST data. This prevents data from being posted twice if a
			# user hits the back button
			return HttpResponseRedirect('/home')

		else:
			# User provided bad credentials
			print("Invalid login credentials: {0}, {1}".format(username, password))
			return HttpResponse("Invalid login details supplied.")	
			
	else:
		# Request is not a POST, so display the login form
		return render(request, 'MusicVoteApp/login.html')	

def home(request):
	# Need to show all of the channels that you can connect to...
	channel_list = MusicChannel.objects.order_by('channel_name')

	if (request.method == 'POST'):
		create_channel_form = CreateChannelForm(data = request.POST)

		if (create_channel_form.is_valid()):
			print("form has valid information")
			
			channel = create_channel_form.save(commit = False)
			channel.creation_date = datetime.now()
			channel.save()

			# Reverse avoids having to hardcode a URL 
			return HttpResponseRedirect(reverse('musicchannel', args = (channel.slug,)))
			
		else:
			print(create_channel_form.errors)

	else:
		create_channel_form = CreateChannelForm()

	return render(request,
				'MusicVoteApp/home.html',
				{'user': request.user, 'form': create_channel_form, 'channel_list': channel_list})

def music_channel(request, music_channel_slug):
	context_dict = {}

	if (request.method == 'POST'):
		# Get the form data and check if its valid
		# if its valid, set the channel id and save
		new_song_form = AddChannelSongForm(data = request.POST)

		if (new_song_form.is_valid()):
			print("form has valid information")
			
			channel = MusicChannel.objects.get(slug = music_channel_slug)

			# TODO: encapsulate some of this logic in the model, "thick models, thin views"
			new_song = new_song_form.save()
			channel.channel_songs.add(new_song)
			new_song_form = AddChannelSongForm()

			context_dict['new_song_form'] = new_song_form
			context_dict['channel'] = channel
			context_dict['songs']	= channel.get_songs()
			
		else:
			print(create_channel_form.errors)

	else:
		try:
			# Try and find a music channel name slug with the given name
			channel = MusicChannel.objects.get(slug = music_channel_slug)
			context_dict['channel'] = channel

			songs = channel.get_songs()
			context_dict['songs'] = songs

			# Construct the a form to allow a user to enter a song for the channel
			new_song_form = AddChannelSongForm()
			context_dict['new_song_form'] = new_song_form

		except (KeyError, MusicChannel.DoesNotExist):
			raise Http404("MusicChannel does not exist")

	return render(request, 'MusicVoteApp/musicchannel.html', context_dict)