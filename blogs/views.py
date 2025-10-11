# from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
    ListView,
)
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import FormMixin

from blogs.decorators import post_ownership_required

from .models import Post
from .forms import PostCreationForm


class PostListView(ListView):
    model = Post
    context_object_name = "post_list"
    template_name = "blogs/list.html"
    paginate_by = 25

    # 각 카테고리 4개만 노출
    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        # 특정 카테고리를 필터링 (예: '여행'이라는 카테고리 ID가 1이라고 가정)
        # 각 카테고리별 최신 4개의 게시물 가져오기
        context["health_posts_4pcs"] = Post.objects.filter(categories__name="건강")[:4]
        context["travel_posts_4pcs"] = Post.objects.filter(categories__name="여행")[:4]
        context["food_beverage_posts_4pcs"] = Post.objects.filter(
            categories__name="음식"
        )[:4]
        context["fashion_beauty_posts_4pcs"] = Post.objects.filter(
            categories__name="패션/뷰티"
        )[:4]
        context["miscellaneous_posts_4pcs"] = Post.objects.filter(
            categories__name="그외다양한주제"
        )[:4]
        return context


# 카테고리별 전체 게시물을 보여줄 뷰
class CategoryPostListView(ListView):
    model = Post
    template_name = "blogs/category_list.html"
    context_object_name = "posts"
    paginate_by = 10  # 페이지당 10개의 게시물

    def get_queryset(self):
        # URL에서 전달된 카테고리 이름으로 필터링
        # category_name에서 슬래시(/)를 하이픈(-)으로 변경하여 URL을 생성 (슬래시(/)를 URL에서 처리하기 어렵기 때문에, 슬래시를 -와 같은 문자로 대체하는 방법)
        category_name = self.kwargs.get("category_name").replace("-", "/")
        return Post.objects.filter(categories__name=category_name)

    def get_context_data(self, **kwargs):
        context = super(CategoryPostListView, self).get_context_data(**kwargs)
        context["category_name"] = self.kwargs.get("category_name")
        return context


class PostDetailView(DetailView):
    model = Post
    context_object_namae = "post"
    template_name = "blogs/detail.html"

    # 이 get_context_data 부분은 검증안된 메소드임(쓰임이 있을 지 모르겠음)
    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context["category_name"] = self.kwargs.get("category_name")
        return context


# 게시글 작성할때는 로그인이 되어 있어야 함(데코레이터 사용)
@method_decorator(login_required, "get")
@method_decorator(login_required, "post")
class PostCreateView(CreateView):
    model = Post
    form_class = PostCreationForm
    template_name = "blogs/create.html"

    # 서버에서 직접 `author`값을 지정하기 위해 form_valid를 오버라이딩해서 user값을 author에 추가
    def form_valid(self, form):
        temp_post = form.save(commit=False)
        temp_post.author = self.request.user
        temp_post.save()

        # categories 필드에 다중 카테고리를 설정
        categories = form.cleaned_data["categories"]
        temp_post.categories.set(
            categories
        )  # 이제 categories는 쿼리셋이므로 그대로 사용 가능

        return super().form_valid(form)

    # success_url 메소드로 오버라이딩해줄텐데, 게시글이 완성이 되면 게시글 detailview로 연결을 시켜줌
    def get_success_url(self):
        return reverse("blogs:detail", kwargs={"pk": self.object.pk})


# 이 customized 메소드 데코레이션은 주인이 맞는 지 확인하는 과정(데코레이터 사용)
@method_decorator(post_ownership_required, "get")
@method_decorator(post_ownership_required, "post")
class PostUpdateView(UpdateView):
    model = Post
    context_object_name = "target_post"
    form_class = PostCreationForm
    template_name = "blogs/update.html"

    # get_success_url 메소드로 오버라이딩해줄텐데, 게시글이 완성이 되면 게시글 detailView로 연결을 시켜줌
    def get_success_url(self):
        return reverse("blogs:detail", kwargs={"pk": self.object.pk})


class PostDeleteView(DeleteView):
    pass
