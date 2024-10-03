from django.urls import path
from .views import RegisterView, LoginView, LogoutView, ChangePasswordView, ProfileView, DeleteUserView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('login/refresh', TokenRefreshView.as_view()),
    path('logout', LogoutView.as_view()),
    path('change_password', ChangePasswordView.as_view()),
    path('profile/<int:pk>', ProfileView.as_view()),
    path('delete/<int:pk>', DeleteUserView.as_view()),
]
