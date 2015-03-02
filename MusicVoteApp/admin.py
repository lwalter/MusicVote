from django.contrib import admin
from MusicVoteApp.models import MusicChannel

class MusicChannelAdmin(admin.ModelAdmin):
	list_display = ('channel_name', 'creation_date')
	list_filter = ['channel_name', 'creation_date']
	search_fields = ['channel_name']
	#prepopulated_fields = {'slug': ('channel_name',)}

	fieldsets = [
		('Date information', {'fields': ['creation_date'], 'classes': ['collapse']}),
		(None,				 {'fields': ['channel_name']}),
	]

admin.site.register(MusicChannel, MusicChannelAdmin)
