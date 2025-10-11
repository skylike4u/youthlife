from django.forms import ModelForm
from django import forms
from articles.models import Article

from projects.models import Project


class ArticleCreationForm(ModelForm):

    # medium-edior 사용을 위한 커스터마이징(해당 html태그에 editable 클래스를 넣어둔다. attrs(attributes)에 class랑 style같은 것은 넣는게 content 필드가 만들어질때 forms에서 설정해서 클래스랑 스타일을 미리 결정해준다.)
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "editable text-start", "style": "height: auto;"}
        )
    )

    project = forms.ModelChoiceField(queryset=Project.objects.all(), required=False)

    class Meta:
        model = Article
        fields = ["title", "image", "project", "content"]
