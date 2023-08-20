from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('player/', include('player.urls')),
    path('quickmatch/', include('quickmatch.urls')),
    path('board/', include('board.urls')),
]
