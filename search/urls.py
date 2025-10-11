from django.urls import path  # URL 패턴을 설정하기 위해 path 함수 사용
from .views import search_view, download_excel

app_name = "search"

# routing
urlpatterns = [
    path("", search_view, name="search"),
    path("download_excel/", download_excel, name="download"),
]
