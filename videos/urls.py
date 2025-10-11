from django.urls import path
from .views import VideoListView

app_name = "videos"

# routing
urlpatterns = [
    path("list/", VideoListView.as_view(), name="list"),
]
