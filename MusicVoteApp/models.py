from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class MusicChannelSong(models.Model):
    song_url = models.URLField(max_length = 200)
    video_id = models.CharField(max_length = 100)
    votes = models.IntegerField(default = 0)

    def increment_votes(self):
        self.votes += 1
        self.save()
        return self.votes

    def slice_video_id(self):
        return self.song_url.split("v=")[1]

    def save(self, *args, **kwargs):
        if self.video_id == "": 
            self.video_id = self.slice_video_id()

        super(MusicChannelSong, self).save(*args, **kwargs)

    def __unicode__(self):
        return "{0}".format(self.video_id)

class MusicChannel(models.Model):
    channel_name = models.CharField(max_length = 50, unique = True)
    creation_date = models.DateTimeField('date created')
    slug = models.SlugField(unique = True)
    channel_songs = models.ManyToManyField(MusicChannelSong)

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
            return self.channel_songs.order_by('votes').first()

    def add_song(self, new_song):
        self.channel_songs.add(new_song)

    def remove_song(self, song_id):
        if self.channel_songs is not None:
            try:
                self.channel_songs.get(id=song_id).delete()
            except Exception as e:
                print "Could not delete song: {0}".format()

    def get_songs(self):
        return self.channel_songs.order_by('votes').all()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.channel_name)
        super(MusicChannel, self).save(*args, **kwargs)

    def __unicode__(self):
        return "{0}".format(self.channel_name)

class Message(models.Model):
    message_text = models.TextField()
    posted_by = models.ForeignKey(User)
    channel_name = models.ForeignKey(MusicChannel)
    date_posted = models.DateTimeField('date posted')
    
    def __unicode__(self):
        return "{0} [{1}]: {2}".format(self.posted_by, self.date_posted, self.message_text)