from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.shortcuts import render
from django.urls import reverse_lazy, reverse

# from profiles.decorators import profile_ownership_required
# from django.utils.decorators import method_decorator

from news.views import News


class NewsListView(ListView):
    model = News
    context_object_name = "news_list"
    template_name = "news/list.html"
    paginate_by = 25


class NewsDetailView(DetailView):
    """News Detail View"""

    model = News
    context_object_name = "target_news"
    template_name = "news/detail.html"
