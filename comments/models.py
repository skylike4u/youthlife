from django.db import models
from users.models import User
from common.models import CommonModel  # created_at/updated_at 등 이미 포함
from articles.models import Article
from blogs.models import Post

# 권장 구현(두 모델 분리 + 추상 베이스)
# 공통 필드를 추상 베이스로 묶고, 각각의 코멘트 모델을 얹는 방식


# 공통 베이스
class BaseComment(CommonModel):

    content = models.TextField(null=False)

    class Meta:
        abstract = True
        ordering = ["-created_at"]


# article comment 모델
class ArticleComment(BaseComment):
    writer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="article_comments"
    )

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,  # 보통 댓글은 부모 삭제 시 함께 삭제 권장
        related_name="article_comments",  # article.comments
    )

    def __str__(self):
        return f"Comment by {self.writer} on {self.article}"


# Post comment 모델
class PostComment(BaseComment):
    writer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="post_comments"
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="post_comments",  # post.comments
    )

    def __str__(self):
        return f"Comment by {self.writer} on {self.post}"
