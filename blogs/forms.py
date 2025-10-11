from django.forms import ModelForm
from django import forms
from blogs.models import Post, Category


class PostCreationForm(ModelForm):

    # medium-edior 사용을 위한 커스터마이징(해당 html태그에 editable 클래스를 넣어둔다. attrs(attributes)에 class랑 style같은 것은 넣는게 content 필드가 만들어질때 forms에서 설정해서 클래스랑 스타일을 미리 결정해준다.)
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "editable text-start",
                "style": "height: auto;",
            },
        ),
        label="◎ 포스트 본문내용(Main contents)",
    )

    # 카테고리 필드를 다중 선택 가능하게 설정 (ModelMultipleChoiceField 사용)
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        required=True,  # 카테고리 선택 필수 처리
        widget=forms.CheckboxSelectMultiple,  # 여러 개의 카테고리를 선택 가능하게 체크박스로 렌더링
        label="◎ 카테고리(*1개만 선택해주세요)",
    )

    class Meta:
        model = Post
        fields = [
            "title",
            "categories",
            "excerpt",
            "content",
            "featured_image",
            "file_upload",
        ]
        # Alternatively, override labels in the Meta class (this applies to fields not customized above)
        labels = {
            "title": "◎ 제 목",
            "excerpt": "◎ 부제 또는 한줄 요약 (Sub-title or Excerpt)",
            "featured_image": "◎ 메인 이미지",
            "file_upload": "◎ 파일 업로드(필요시)",
        }
