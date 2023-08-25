from django.contrib import admin
from .models import User, DMRoom, DirectMessage


admin.site.register(User)
admin.site.register(DMRoom)
admin.site.register(DirectMessage)
