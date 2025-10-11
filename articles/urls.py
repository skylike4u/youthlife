from django.views.generic import TemplateView
from django.urls import path

from articles.views import (
    ArticleCreateView,
    ArticleDetailView,
    ArticleUpdateView,
    ArticleDeleteView,
    ArticleListView,
)

from . import views

app_name = "articles"

# routing
urlpatterns = [
    path("list/", ArticleListView.as_view(), name="list"),
    path("create/", ArticleCreateView.as_view(), name="create"),
    path("detail/<int:pk>", ArticleDetailView.as_view(), name="detail"),
    path("update/<int:pk>", ArticleUpdateView.as_view(), name="update"),
    path("delete/<int:pk>", ArticleDeleteView.as_view(), name="delete"),
]
