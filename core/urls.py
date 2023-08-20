from django.contrib import admin
from django.urls import path, include

# img module import
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('player/', include('player.urls')),
    path('quickmatch/', include('quickmatch.urls')),
    path('board/', include('board.urls')),
]

#img
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDAI_ROOT)
