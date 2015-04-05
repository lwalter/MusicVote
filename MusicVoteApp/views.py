from datetime import datetime
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from MusicVoteApp.models import MusicChannel, MusicChannelSong, Message
from MusicVoteApp.forms import UserForm, CreateChannelForm, AddChannelSongForm

def index(request):
    """ Handles index requests. """

    # If user is already authenticated then redirect to the home page
    if request.user.is_authenticated():
        return HttpResponseRedirect('/home')
    else:
        return render(request, 'MusicVoteApp/index.html')

# Use decorator to ensure that only those who are logged in can see the view
@login_required
def logout_user(request):
    """ Handles requests for logging out a user. """
    logout(request)
    return HttpResponseRedirect('/')

def register(request):
    """ Handles requests on the register page. """

    # Set registered flag to false initially
    registered = False

    # If its an HTTP POST, lets process the forms data
    if request.method == 'POST':
        form = UserForm(data=request.POST)

        # If the form is valid...
        if form.is_valid():
            # Save the users form to the database
            user = form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print form.errors
    else:
        form = UserForm()

    return render(request, 'MusicVoteApp/register.html', {'form': form, 'registered': registered})

def login_user(request):
    """ Handles requests for the login page. """

    if request.method == 'POST':
        # Get the users info and attempt to login
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            # User provided valid credentials
            login(request, user)

            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the back button
            return HttpResponseRedirect('/home')
        else:
            # User provided bad credentials
            print "Invalid login credentials: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")       
    else:
        # Request is not a POST, so display the login form
        return render(request, 'MusicVoteApp/login.html')   

@login_required
def home(request):
    """ Handles requests for the home page. """

    # Need to show all of the channels that you can connect to...
    channel_list = MusicChannel.objects.order_by('channel_name')

    if request.method == 'POST':
        create_channel_form = CreateChannelForm(data=request.POST)

        if create_channel_form.is_valid():
            channel = create_channel_form.save(commit=False)
            channel.creation_date = datetime.now()
            channel.owner = request.user
            channel.save()

            # Reverse avoids having to hardcode a URL w/ params
            return HttpResponseRedirect(reverse('musicchannel', args=(channel.slug,)))
        else:
            print create_channel_form.errors
    else:
        create_channel_form = CreateChannelForm()

    return render(request, 'MusicVoteApp/home.html', {'user': request.user, 'form': create_channel_form, 'channel_list': channel_list})

@login_required
def music_channel(request, music_channel_slug):
    """ Handles requests for music channels.  """

    context_dict = {}

    if request.method == 'POST':
        # Get the form data and check if its valid
        # if its valid, set the channel id and save
        new_song_form = AddChannelSongForm(data=request.POST)
        channel = MusicChannel.objects.get(slug=music_channel_slug)
        songs = channel.get_songs()

        context_dict['new_song_form'] = new_song_form
        context_dict['channel'] = channel
        context_dict['songs'] = songs
        context_dict['is_owner'] = channel.is_owner(request.user)
        context_dict['messages'] = channel.messages.order_by('date_posted').all()
        
        if new_song_form.is_valid():
            new_song = new_song_form.save(commit=False)

            if not channel.song_exists(new_song.song_url):
                new_song.save()
                channel.channel_songs.add(new_song)
                new_song_form = AddChannelSongForm()
        else:
            print new_song_form.errors

        context_dict['song_to_play'] = channel.get_first_song()
    else:
        try:
            # Try and find a music channel name slug with the given name
            new_song_form = AddChannelSongForm()
            channel = MusicChannel.objects.get(slug=music_channel_slug)
            songs = channel.get_songs()

            context_dict['new_song_form'] = new_song_form
            context_dict['channel'] = channel
            context_dict['songs'] = songs
            context_dict['song_to_play'] = channel.get_first_song()
            context_dict['is_owner'] = channel.is_owner(request.user)
            context_dict['messages'] = channel.messages.order_by('date_posted').all()
        except KeyError, MusicChannel.DoesNotExist:
            raise Http404("MusicChannel does not exist")

    return render(request, 'MusicVoteApp/musicchannel.html', context_dict)

@login_required
def vote(request):
    """ Handles voting posts for songs. """

    if request.is_ajax() and 'musicchannel' in request.POST and 'song' in request.POST:
        musicchannel_id = request.POST.get('musicchannel')
        song_id = request.POST.get('song')

        try:
            musicchannel = MusicChannel.objects.get(id=musicchannel_id)
            song = musicchannel.get_song_by_pk(song_id)
            votes = song.increment_votes()
        except Exception as e:
            # TODO need to update votes element on page
            # TODO parse out exceptions (DoesNotExist, multiple returns?)
            print e.message
    
    return JsonResponse({'votes': votes, 'song_id': song.id})

@login_required
def get_next_song(request):
    """ Handles an AJAX GET request for when a song ends and retrieves the next song. """

    if request.is_ajax() and 'musicchannel' in request.GET and 'song' in request.GET:
        musicchannel_id = request.GET.get('musicchannel')
        song_id = request.GET.get('song')

        try:
            # Try and locate the music channel and song to remove
            musicchannel = MusicChannel.objects.get(id=musicchannel_id)
            song = musicchannel.get_song_by_video_id(song_id)
            musicchannel.remove_song(song.id)
    
            # Try and get the next song to play
            next_song = musicchannel.get_first_song()
            next_video_id = next_song.video_id
        except Exception as e:
            print e.message
            next_video_id = ""

    return JsonResponse({'song_to_play': next_video_id})

@login_required
def send_message(request):
    """ Handles an AJAX POST request to send a chat message. """

    if request.is_ajax() and 'musicchannel' in request.POST and 'message' in request.POST:
        musicchannel_id = request.POST.get('musicchannel')
        message_text = request.POST.get('message')

        try:
            musicchannel = MusicChannel.objects.get(id=musicchannel_id)
            message = Message(message_text=message_text, posted_by=request.user, date_posted=datetime.now())
            message.save()
            musicchannel.add_message(message)
        except Exception as e:
            print e.message

    return JsonResponse({'message': message.get_html()})

def polling(request):
    """ Handles the AJAX GET polling request. Retrieves messages and playlist. """

    if request.is_ajax() and 'musicchannel' in request.GET:
        musicchannel_id = request.GET.get('musicchannel')

        try:
            musicchannel = MusicChannel.objects.get(id=musicchannel_id)
            playlist_html = musicchannel.generate_playlist_html()
            messages_html = musicchannel.generate_message_html()
        except Exception as e:
            print e.message

    return JsonResponse({'messages': messages_html, 'playlist': playlist_html})