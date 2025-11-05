from django.urls import reverse
from django.views.generic import CreateView, DeleteView
from django.utils.decorators import method_decorator
from articles.models import Article
from blogs.models import Post
from comments.forms import ArticleCommentCreationForm, PostCommentCreationForm
from comments.models import ArticleComment, PostComment
from comments.decorators import (
    article_comment_ownership_required,
    post_comment_ownership_required,
)


# Article comment 부분
class ArticleCommentCreateView(CreateView):
    model = ArticleComment
    form_class = ArticleCommentCreationForm
    template_name = "comments/article_create.html"

    def form_valid(self, form):
        temp_comment = form.save(commit=False)
        # create.html에서 hidden으로 보내서 받은 article_pk를 temp_comment.article로 넘기는 것
        # 또, request에서 받은 POST데이터 중에서, article_pk라는 데이터를 통해서 temp_comment의 article 값으로 설정해주는 것
        temp_comment.article = Article.objects.get(pk=self.request.POST["article_pk"])
        temp_comment.writer = self.request.user
        temp_comment.save()
        return super().form_valid(form)

    # 작업이 성공하면 어디로 돌아갈건지 설정해줌  / 또 여기에 self.object는 articlecomment겠죠. object(articlecomment)의 article의 pk
    # 여기 현재 object는 comment를 뜻한다.
    def get_success_url(self):
        return reverse("articles:detail", kwargs={"pk": self.object.article.pk})


@method_decorator(article_comment_ownership_required, "get")
@method_decorator(article_comment_ownership_required, "post")
class ArticleCommentDeleteView(DeleteView):
    model = ArticleComment
    context_object_name = "target_comment"
    template_name = "comments/article_delete.html"

    # 댓글을 삭제하고 나서 어디로 url로 가냐 (해당 article을 가진 pk로 되돌아가라)
    def get_success_url(self):
        return reverse("articles:detail", kwargs={"pk": self.object.article.pk})


# Post comment 부분
class PostCommentCreateView(CreateView):
    model = PostComment
    form_class = PostCommentCreationForm
    template_name = "comments/post_create.html"

    def form_valid(self, form):
        temp_comment = form.save(commit=False)
        # post_create.html에서 hidden으로 보내서 받은 post_pk를 temp_comment.post로 넘기는 것
        # 또, request에서 받은 POST데이터 중에서, post_pk라는 데이터를 통해서 temp_comment의 post 값으로 설정해주는 것
        temp_comment.post = Post.objects.get(pk=self.request.POST["post_pk"])
        temp_comment.writer = self.request.user
        temp_comment.save()
        return super().form_valid(form)

    # 작업이 성공하면 어디로 돌아갈건지 설정해줌  / 또 여기에 self.object는 postcomment겠죠. object(postcomment)의 post의 pk
    # 여기 현재 object는 postcomment를 뜻한다.
    def get_success_url(self):
        return reverse("blogs:detail", kwargs={"pk": self.object.post.pk})


@method_decorator(post_comment_ownership_required, "get")
@method_decorator(post_comment_ownership_required, "post")
class PostCommentDeleteView(DeleteView):
    model = PostComment
    context_object_name = "target_comment"
    template_name = "comments/post_delete.html"

    # 댓글을 삭제하고 나서 어디로 url로 가냐 (해당 post을 가진 pk로 되돌아가라)
    def get_success_url(self):
        return reverse("blogs:detail", kwargs={"pk": self.object.post.pk})
