from django.urls import path
from .views import DvrListCreateView, DvrRetrieveUpdateDestroyView

urlpatterns = [
    path('', DvrListCreateView.as_view(), name='list_create_dvr_info'),  # Đường dẫn cho API
    path('<int:pk>/', DvrRetrieveUpdateDestroyView.as_view(), name='retrieve_update_delete_dvr_info'),  # Đường dẫn cho API
]
