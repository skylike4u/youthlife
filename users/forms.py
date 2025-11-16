from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User  # 커스텀 유저


# 회원가입 정보 확장 / UserCreationForm을 상속받아서 커스터마이징함
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User  # ✅ 반드시 커스텀 유저로 지정
        fields = UserCreationForm.Meta.fields
        # 필요하면 직접 지정: fields = ("username", "email",)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = UserChangeForm.Meta.fields


# UserCreationForm을 상속받아서 커스터마이징함
class AccountUpdateForm(UserCreationForm):
    """초기화 이후에 username을 비활성화시키는 구문"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # username칸을 비활성화 시켜줌
        self.fields["username"].disabled = True
