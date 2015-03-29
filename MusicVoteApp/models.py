import urllib2
import xmltodict
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class MusicChannelSong(models.Model):
    song_url = models.URLField(max_length=200)
    video_id = models.CharField(max_length=100)
    votes = models.IntegerField(default=0)
    title = models.CharField(max_length=200)

    def increment_votes(self):
        self.votes += 1
        self.save()
        return self.votes

    def slice_video_id(self):
        return self.song_url.split("v=")[1]

    def retrieve_title(self):
        if self.video_id != "":
            video_xml = urllib2.urlopen("http://gdata.youtube.com/feeds/api/videos/{0}?v=2&fields=title".format(self.video_id))
            
            try:
                data = video_xml.read()
                video_xml.close()
            except Exception as e:
                print e.message

            data = xmltodict.parse(data)
            return data.get('entry').get('title')

    def save(self, *args, **kwargs):
        if self.video_id == "": 
            self.video_id = self.slice_video_id()

        if self.title == "":
            self.title = self.retrieve_title()

        super(MusicChannelSong, self).save(*args, **kwargs)

    def __unicode__(self):
        return "{0}".format(self.video_id)
        
class Message(models.Model):
    message_text = models.TextField(blank=False)
    posted_by = models.ForeignKey(User, blank=False)
    date_posted = models.DateTimeField('date posted')

    def get_html(self):
        return "<li>{0}: {1}</li>".format(self.posted_by, self.message_text)

    def __unicode__(self):
        return "{0} {1}: {2}".format(self.posted_by, self.date_posted, self.message_text)

class MusicChannel(models.Model):
    channel_name = models.CharField(max_length=50, unique=True)
    creation_date = models.DateTimeField('date created')
    slug = models.SlugField(unique=True)
    channel_songs = models.ManyToManyField(MusicChannelSong)
    #users = models.ManyToManyField(User)
    owner = models.ForeignKey(User, blank=False)
    messages = models.ManyToManyField(Message)

    def song_exists(self, song_url):
        song_exists = False
        if self.channel_songs is not None:
            if self.channel_songs.filter(song_url=song_url).count() > 0:
                song_exists = True

        return song_exists

    def get_song_by_pk(self, song_id):
        if self.channel_songs is not None:
            return self.channel_songs.get(id=song_id)

    def get_song_by_video_id(self, video_id):
        if self.channel_songs is not None:
            return self.channel_songs.get(video_id=video_id)

    def get_first_song(self):
        if self.channel_songs is not None:
            return self.channel_songs.order_by('-votes').first()

    def add_song(self, new_song):
        self.channel_songs.add(new_song)

    def remove_song(self, song_id):
        removed = False
        if self.channel_songs is not None:
            try:
                self.channel_songs.get(id=song_id).delete()
                removed = True
            except Exception as e:
                print "Could not delete song: {0}".format()

        return removed

    def get_songs(self):
        return self.channel_songs.order_by('-votes').all()

    """def add_user(self, user):
        self.users.add(user)

    def remove_user(self, user):
        removed = False
        if self.users is not None:
            try:
                self.users.get(id=user.id).delete()
                removed = True
            except Exception as e:
                print e.message

        return removed

    def get_users(self):
        return self.users.all()
    """
    def is_owner(self, user):
        return self.owner == user

    def add_message(self, new_message):
        self.messages.add(new_message)

    def generate_message_html(self):
        html = ""
        
        if self.messages is not None:
            for msg in self.messages.all():
                html += msg.get_html()

        return html

    def save(self, *args, **kwargs):
        self.slug = slugify(self.channel_name)
        super(MusicChannel, self).save(*args, **kwargs)

    def __unicode__(self):
        return "{0}".format(self.channel_name)