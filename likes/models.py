from django.db import models
from users.models import User

from articles.models import Article


class Like(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="liked_records"
    )
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="likes")

    # Meta클래스를 통해, user와 article이 한쌍만 존재하도록 튜플로 설정
    class Meta:
        unique_together = ("user", "article")
