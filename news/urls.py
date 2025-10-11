from django.urls import path

from news.views import NewsListView, NewsDetailView

app_name = "news"

# routing
urlpatterns = [
    path("news/", NewsListView.as_view(), name="list"),
    path("news/<int:pk>", NewsDetailView.as_view(), name="detail"),
]
