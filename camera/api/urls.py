from django.urls import path, include
from .ping import urls as ping
from .dvr_info import urls as dvr
from .channel_info import urls as channel

urlpatterns = [
    path('ping', include(ping)),
    path('dvr/', include(dvr)),
    path('channel/', include(channel)),
]
