from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    # when navigating to this url, a new ChatConsumer instance will be made
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]