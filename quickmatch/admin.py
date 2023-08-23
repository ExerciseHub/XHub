from django.contrib import admin
from .models import Meeting, MeetingChat, MeetingMembers


admin.site.register(Meeting)
admin.site.register(MeetingChat)
admin.site.register(MeetingMembers)
