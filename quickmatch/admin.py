from django.contrib import admin
from .models import Meeting, MeetingMessage, MeetingMembers, MeetingRoom


admin.site.register(Meeting)
admin.site.register(MeetingMembers)
admin.site.register(MeetingRoom)
admin.site.register(MeetingMessage)
