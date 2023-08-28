from django.contrib import admin
from .models import User, DirectMessage, DMRoom


admin.site.register(User)
admin.site.register(DirectMessage)
admin.site.register(DMRoom)
