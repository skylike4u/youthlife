from django.urls import path

from likes.views import LikeArticleView

app_name = "likes"

urlpatterns = [
    path("article/like/<int:pk>", LikeArticleView.as_view(), name="article_like"),
]
