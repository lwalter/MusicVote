from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class MusicChannelSong(models.Model):
	song_name = models.CharField(max_length = 50)
	song_url  = models.URLField(max_length = 200)

	def __unicode__(self):
		return "{0}".format(self.song_url)

class MusicChannel(models.Model):
	channel_name  = models.CharField(max_length = 20, unique = True)
	creation_date = models.DateTimeField('date created')
	slug		  = models.SlugField(unique = True)
	channel_songs = models.ManyToManyField(MusicChannelSong)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.channel_name)
		super(MusicChannel, self).save(*args, **kwargs)

	def __unicode__(self):
		return "{0} ({1})".format(self.channel_name, ", ".join([song.song_name
																 for song in self.channel_songs.all()]))

class Message(models.Model):
	message_text = models.TextField()
	posted_by    = models.ForeignKey(User)
	channel_name = models.ForeignKey(MusicChannel)
	date_posted  = models.DateTimeField('date posted')
	
	def __unicode__(self):
 		return "{0} [{1}]: {2}".format(self.posted_by, self.date_posted, self.message_text)