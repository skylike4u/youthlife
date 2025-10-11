from django.contrib import admin
from blogs.models import Post, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Category Admin Definition"""

    list_display = ("name", "slug")


@admin.register(Post)
class BlogAdmin(admin.ModelAdmin):
    """Blog Admin Definition"""

    list_display = ("title", "author", "created_at", "updated_at")
