from django.urls import path
from comments.views import CommentCreateView, CommentDeleteView

app_name = "comments"

# routing
urlpatterns = [
    path("create/", CommentCreateView.as_view(), name="create"),
    path("delete/<int:pk>", CommentDeleteView.as_view(), name="delete"),
]
