from django.db import models
from users.models import User
from common.models import CommonModel
from articles.models import Article


# Create your models here.
class Comment(CommonModel):
    article = models.ForeignKey(
        Article, on_delete=models.SET_NULL, null=True, related_name="comment"
    )
    writer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="comment"
    )
    content = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now=True)
