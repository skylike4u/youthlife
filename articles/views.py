# from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
    ListView,
)
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import FormMixin

from articles.decorators import article_ownership_required

from articles.forms import ArticleCreationForm
from comments.forms import CommentCreationForm
from .forms import ArticleCreationForm
from articles.models import Article


# 게시글 작성할때는 로그인이 되어 있어야 함(데코레이터 사용)
@method_decorator(login_required, "get")
@method_decorator(login_required, "post")
class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleCreationForm
    template_name = "articles/create.html"

    # 서버에서 직접 writer값을 지정하기 위해 form_valid를 오버라이딩해서 user값을 writer에 추가
    def form_valid(self, form):
        temp_article = form.save(commit=False)
        temp_article.writer = self.request.user
        temp_article.save()
        return super().form_valid(form)

    # success_url 메소드로 오버라이딩해줄텐데, 게시글이 완성이 되면 게시글 detailview로 연결을 시켜줌
    def get_success_url(self):
        return reverse("articles:detail", kwargs={"pk": self.object.pk})


class ArticleDetailView(DetailView, FormMixin):
    model = Article
    form_class = CommentCreationForm
    context_object_name = "target_article"
    template_name = "articles/detail.html"


# 이 메소드 데코레이션은 주인이 맞는 지 확인하는 과정
# 게시글 작성할때는 로그인이 되어 있어야 함(데코레이터 사용)
@method_decorator(article_ownership_required, "get")
@method_decorator(article_ownership_required, "post")
class ArticleUpdateView(UpdateView):
    model = Article
    context_object_name = "target_article"
    form_class = ArticleCreationForm
    template_name = "articles/update.html"

    # get_success_url 메소드로 오버라이딩해줄텐데, 게시글이 완성이 되면 게시글 detailView로 연결을 시켜줌
    def get_success_url(self):
        return reverse("articles:detail", kwargs={"pk": self.object.pk})


# 이 메소드 데코레이션은 주인이 맞는 지 확인하는 과정
# 게시글 작성할때는 로그인이 되어 있어야 함(데코레이터 사용)
@method_decorator(article_ownership_required, "get")
@method_decorator(article_ownership_required, "post")
class ArticleDeleteView(DeleteView):
    model = Article
    context_object_name = "target_article"
    success_url = reverse_lazy("articles:list")
    template_name = "articles/delete.html"


class ArticleListView(ListView):
    model = Article
    context_object_name = "article_list"
    template_name = "articles/list.html"
    paginate_by = 25

    def get_queryset(self):
        return Article.objects.all().order_by("-pk")
