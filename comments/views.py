from django.urls import reverse
from django.views.generic import CreateView, DeleteView
from django.utils.decorators import method_decorator


from articles.models import Article
from comments.forms import CommentCreationForm
from comments.models import Comment
from comments.decorators import comment_ownership_required


class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentCreationForm
    template_name = "comments/create.html"

    def form_valid(self, form):
        temp_comment = form.save(commit=False)
        # create.html에서 hidden으로 보내서 받은 article_pk를 temp_comment.article로 넘기는 것
        # 또, request에서 받은 POST데이터 중에서, article_pk라는 데이터를 통해서 temp_comment의 article 값으로 설정해주는 것
        temp_comment.article = Article.objects.get(pk=self.request.POST["article_pk"])
        temp_comment.writer = self.request.user
        temp_comment.save()
        return super().form_valid(form)

    # 작업이 성공하면 어디로 돌아갈건지 설정해줌  / 또 여기에 self.object는 comment겠죠. object(comment)의 article의 pk
    # 여기 현재 object는 comment를 뜻한다.
    def get_success_url(self):
        return reverse("articles:detail", kwargs={"pk": self.object.article.pk})


@method_decorator(comment_ownership_required, "get")
@method_decorator(comment_ownership_required, "post")
class CommentDeleteView(DeleteView):
    model = Comment
    context_object_name = "target_comment"
    template_name = "comments/delete.html"

    # 댓글을 삭제하고 나서 어디로 url로 가냐 (해당 article을 가진 pk로 되돌아가라)
    def get_success_url(self):
        return reverse("articles:detail", kwargs={"pk": self.object.article.pk})
