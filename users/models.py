from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    class GenderChoices(models.TextChoices):
        # 첫번째는 데이터베이스에 들어갈 value이고, 그 다음은 관리자페이지에서 보게 되는 label이 될것이다.
        MALE = ("male", "Male")
        FEMALE = ("female", "Female")

    # (유령필드로 만들기) AbstractUser클래스에서 있는 first_name, last_name을 쓰지않게 만듦(유령 필드로 만듦 / last-first name 한국에서는 쓰지않는 방식)
    first_name = models.CharField(
        max_length=150,
        editable=False,
    )
    last_name = models.CharField(
        max_length=150,
        editable=False,
    )
    # blank=True는 form에서 필드가 필수적이지 않게 해줌 / Pillow 라이브러리 설치 필요
    avatar = models.ImageField(blank=True)

    # 새로운 name 필드 생성
    name = models.CharField(max_length=150, default="")
    is_host = models.BooleanField(default=False)
    gender = models.CharField(
        max_length=10,
        choices=GenderChoices.choices,
    )
