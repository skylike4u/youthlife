# /api/v1/users/ 하위 DRF 라우팅
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import api_views


# routing
urlpatterns = [
    path("", api_views.Users.as_view()),
    path("me", api_views.Me.as_view()),
    path("change-password", api_views.ChangePassword.as_view()),
    path("@<str:username>", api_views.PublicUser.as_view()),
    path("log-in", api_views.LogIn.as_view()),
    path("log-out", api_views.LogOut.as_view()),
    path("token-login", obtain_auth_token),
    path("jwt-login", api_views.JWTLogIn.as_view()),
]
