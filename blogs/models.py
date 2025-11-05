from django.db import models
from common.models import CommonModel
from users.models import User
from django.utils.text import slugify
import os
from django.urls import reverse
from django.utils import timezone


# 카테고리 모델: 게시물을 카테고리(예: "건강", "여행", "패션")로 구성
class Category(CommonModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# 태그 모델 : 게시물에 키워드(예: "피트니스", "럭셔리")를 태그할 수 있음
class Tag(CommonModel):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(CommonModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    excerpt = models.TextField(max_length=300, blank=True)
    categories = models.ManyToManyField(Category, related_name="posts")
    tags = models.ManyToManyField(Tag, related_name="posts", blank=True)
    published_at = models.DateTimeField(default=timezone.now)
    file_upload = models.FileField(upload_to="files/%Y/%m/%d", blank=True)
    # 게시물과 관련된 기본 이미지에 대한 featured_image
    featured_image = models.ImageField(upload_to="blog_images/", null=True, blank=True)
    # 게시물은 즉시 게시되거나  is_published 플래그를 사용하여 초안으로 설정가능
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["-published_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            original_slug = self.slug
            queryset = Post.objects.filter(slug=self.slug)
            count = 1
            # 중복되는 slug가 있는지 확인하고, 있다면 고유한 slug를 생성
            while queryset.exists():
                self.slug = f"{original_slug}-{count}"
                queryset = Post.objects.filter(slug=self.slug)
                count += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blogs:detail", kwargs={"pk": self.pk})

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    def get_file_ext(self):
        return self.get_file_name().split(".")[-1]


class Subscriber(CommonModel):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
