from django.urls import path
from .views import ChannelListCreateView, ChannelRetrieveUpdateDestroyView

urlpatterns = [
    path('', ChannelListCreateView.as_view(), name='list_create_channel_info'),  # Đường dẫn cho API
    path('<int:pk>/', ChannelRetrieveUpdateDestroyView.as_view(), name='retrieve_update_delete_channel_info'),  # Đường dẫn cho API
]
