from django.urls import path

from projects.views import ProjectListView, ProjectCreateView, ProjectDetailView

app_name = "projects"

# routing
urlpatterns = [
    path("list/", ProjectListView.as_view(), name="list"),
    path("create/", ProjectCreateView.as_view(), name="create"),
    path("detail/<int:pk>", ProjectDetailView.as_view(), name="detail"),
]
