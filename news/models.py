from users.models import User
from django.db import models
import os
from django.urls import reverse


class News(models.Model):
    """News Model Definotion"""

    writer = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="news", null=True
    )
    # policy_field = models.ForeignKey()
    # policy_region = models.ForeignKey()
    # 조회수도 차후에 넣을 것
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to="news/%Y/%m/%d", blank=True)
    file_upload = models.FileField(upload_to="files/%Y/%m/%d", blank=True)
    content = models.TextField(null=True)

    created_at = models.DateField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    # like = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("news:list", kwargs={"pk": self.pk})

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    def get_file_ext(self):
        return self.get_file_name().split(".")[-1]
