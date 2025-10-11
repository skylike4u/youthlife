from django.db import models
from users.models import User
from common.models import CommonModel

# from projects.models import Project

class Article(CommonModel):
    # related_name은 user네임에서 article로 접근할 때 쓰는 속성이기 때문에 직관적으로 article이라고 써줌
    writer = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="article", null=True
    )

    title = models.CharField(max_length=200, null=True)
    image = models.ImageField(upload_to="article/", null=False)
    content = models.TextField(null=True)

    




