from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustumUserAdmin(UserAdmin):
    # 반드시 Tuple형태가 되어야해. 정말 중요해
    fieldsets = (
        (
            "Profile",
            {
                "fields": (
                    "avatar",
                    "username",
                    "password",
                    "name",
                    "email",
                    "is_host",
                    "gender",
                ),
                "classes": ("wide",),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
                # 감추기
                "classes": ("collapse",),
            },
        ),
        (
            "Important Dates",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                ),
                # 감추기
                "classes": ("collapse",),
            },
        ),
    )
    # fields = ("email", "password", "name")

    list_display = (
        "username",
        "email",
        "name",
        "is_host",
    )
