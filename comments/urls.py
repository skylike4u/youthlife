from django.urls import path
from comments import views

app_name = "comments"

# routing
urlpatterns = [
    path(
        "article_create/",
        views.ArticleCommentCreateView.as_view(),
        name="article_create",
    ),
    path(
        "article_delete/<int:pk>",
        views.ArticleCommentDeleteView.as_view(),
        name="article_delete",
    ),
    path(
        "post_create/",
        views.PostCommentCreateView.as_view(),
        name="post_create",
    ),
    path(
        "post_delete/<int:pk>",
        views.PostCommentDeleteView.as_view(),
        name="post_delete",
    ),
]
