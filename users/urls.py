from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import web_views

app_name = "users"

# routing
urlpatterns = [
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("signup/", web_views.UserCreateView.as_view(), name="signup"),
    path("detail/<int:pk>", web_views.UserDetailView.as_view(), name="detail"),
    path("update/<int:pk>", web_views.UserUpdateView.as_view(), name="update"),
    path("delete/<int:pk>", web_views.UserDeleteView.as_view(), name="delete"),
]
