from django.forms import ModelForm
from comments.models import ArticleComment, PostComment


class ArticleCommentCreationForm(ModelForm):
    class Meta:
        model = ArticleComment
        fields = ["content"]


class PostCommentCreationForm(ModelForm):
    class Meta:
        model = PostComment
        fields = ["content"]
