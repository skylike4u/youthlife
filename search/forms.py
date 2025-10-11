from django import forms


# 사용자로부터 검색어를 입력받기 위한 폼 클래스
class SearchForm(forms.Form):
    query = forms.CharField(
        label="네이버 검색 API 기반",
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Enter search term..."}),
    )
    # 검색어를 입력받는 한 개의 필드만 포함, 최대 길이는 100자로 제한
