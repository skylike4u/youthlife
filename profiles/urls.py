from django.urls import path

from profiles.views import ProfileCreateView, ProfileUpdateView

app_name = "profiles"

# routing
urlpatterns = [
    path("create/", ProfileCreateView.as_view(), name="create"),
    path("update/<int:pk>", ProfileUpdateView.as_view(), name="update"),
]
