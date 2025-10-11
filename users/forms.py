from django.contrib.auth.forms import UserCreationForm


# UserCreationForm을 상속받아서 커스터마이징함
class AccountUpdateForm(UserCreationForm):
    """초기화 이후에 username을 비활성화시키는 구문"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # username칸을 비활성화 시켜줌
        self.fields["username"].disabled = True
