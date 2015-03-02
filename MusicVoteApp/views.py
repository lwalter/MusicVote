from django.shortcuts import render_to_response
from django.template import RequestContext
from MusicVoteApp.forms import UserForm, CreateChannelForm, AddChannelSongForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login
from datetime import datetime
from MusicVoteApp.models import MusicChannel, MusicChannelSong

def index(request):
	context = RequestContext(request)
	return render_to_response(
			'MusicVoteApp/index.html', 
			context)

def register(request):
	# Get the requests context
	context = RequestContext(request)

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

	return render_to_response(
			'MusicVoteApp/register.html', 
			{'form': form, 'registered': registered},
			context)

def login_user(request):
	context = RequestContext(request)

	if (request.method == 'POST'):
		print("Was a POST")
		# Get the users info and attempt to login
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username = username, password = password)

		if (user):
			# User provided valid credentials
			login(request, user)
			return HttpResponseRedirect('/home')

		else:
			# User provided bad credentials
			print("Invalid login credentials: {0}, {1}".format(username, password))
			return HttpResponse("Invalid login details supplied.")	
			
	else:
		# Request is not a POST, so display the login form
		print("Was a get")
		return render_to_response(
					'MusicVoteApp/login.html', 
					{}, 
					context)	

def home(request):
	context = RequestContext(request)

	# Need to show all of the channels that you can connect to...
	channel_list = MusicChannel.objects.order_by('channel_name')

	if (request.method == 'POST'):
		create_channel_form = CreateChannelForm(data = request.POST)

		if (create_channel_form.is_valid()):
			print("form has valid information")
			
			channel = create_channel_form.save(commit = False)
			channel.creation_date = datetime.now()
			channel.save()
			
		else:
			print(create_channel_form.errors)

	else:
		create_channel_form = CreateChannelForm()

	return render_to_response(
				'MusicVoteApp/home.html',
				{'user': request.user, 'form': create_channel_form, 'channel_list': channel_list,},
				context)

def music_channel(request, music_channel_slug):
	context = RequestContext(request)
	context_dict = {}

	if (request.method == 'POST'):
		print("it was a post....")

		# get the form data and check if its valid
		# if its valid, set the channel id and save
		new_song_form = AddChannelSongForm(data = request.POST)

		if (new_song_form.is_valid()):
			print("form has valid information")
			
			channel = MusicChannel.objects.get(slug = music_channel_slug)

			new_song = new_song_form.save(commit = False)
			channel.channel_songs.add(new_song)
			
		else:
			print(create_channel_form.errors)

	else:
		print("music channel slug {0}".format(music_channel_slug))
		try:
			# Try and find a music channel name slug with the given name
			channel = MusicChannel.objects.get(slug = music_channel_slug)
			context_dict['channel'] = channel

			# TODO: need to fix this prefetch query theres an issue here
			# Use prefetch_related
			songs = MusicChannelSong.objects.prefetch_related('channel_songs').filter(channel = channel.id)	
			#songs = MusicChannelSong.objects.all().filter(channel = channel.id)
			context_dict['songs'] = songs

			# Construct the a form to allow a user to enter a song for the channel
			new_song_form = AddChannelSongForm()
			context_dict['new_song_form'] = new_song_form

		except MusicChannel.DoesNotExist:
			pass

	return render_to_response(
				'MusicVoteApp/musicchannel.html', 
				context_dict, 
				context)