from django.forms import ModelForm

from profiles.models import Profile


# ModelForm은 기존의 있던 모델(DB)과 연동해서 form으로 생성
class ProfileCreationForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["image", "nickname", "message"]
