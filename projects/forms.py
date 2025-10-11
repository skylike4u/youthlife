from django.forms import ModelForm

from projects.models import Project


class ProjectCreationForm(ModelForm):

    class Meta:
        model = Project
        # 아래 3가지를 입력으로 받게 됨
        fields = ["image", "title", "description"]
