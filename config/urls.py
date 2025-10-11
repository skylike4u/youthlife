from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


# include를 통해 하위분개 실시
urlpatterns = [
    # 기존 웹루트
    path("", include("core.urls")),
    path("admin/", admin.site.urls),
    # 웹(SSR/HTMX) - users
    path("users/", include(("users.web_urls", "users_web"), namespace="users_web")),
    path("search/", include("search.urls", namespace="search")),
    path("articles/", include("articles.urls")),
    path("profiles/", include("profiles.urls")),
    path("comments/", include("comments.urls")),
    path("projects/", include("projects.urls")),
    path("blogs/", include("blogs.urls")),
    path("likes/", include("likes.urls")),
    path("search/", include("search.urls")),
    path("polls/", include("polls.urls")),
    path("videos/", include("videos.urls")),
    # API -  DRF(JSON) 라우팅
    path(
        "api/v1/users/", include(("users.api_urls", "users_api"), namespace="users_api")
    ),
    path("api/v1/articles/", include("articles.urls")),
    path("api/v1/categories/", include("categories.urls")),
    path("api/v1/rooms/", include("rooms.urls")),
]


# 우선 urlpatterns에서 static을 가져와 줌. static의 인자로 settings을 가져와 줌
# DEBUG가 True라면(프로덕션이 아니라 개발중이라면), urlpatterns += (urlpatterns에 += 하나더 추가할거다)
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
