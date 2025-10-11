from users.models import User
from django.db import models
from common.models import CommonModel


class Profile(CommonModel):
    # OneToOneField는 1:1 대응이고, Profile와 user 객체를 하나씩 연결해준다
    # 이름설정 : 이렇게 접근가능 (아래)
    # (view에서 여러 객체를 썻잖아 이렇게 -> request.user.profile) 바로 related_name을 적어놓으면 객체를 바로 받아놓을수 있음
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    # null=True 꼭 프로필 사진을 안올려도 괜찮다는 뜻 (null은 DB하고 연관있음.)
    # upload_to속성은 저장된 이미지가 어디에 저장될 것인지 설정
    image = models.ImageField(upload_to="profiles/", null=True)
    # nickname이 unique로 설정해서 동일한 닉네임 방지
    nickname = models.CharField(max_length=20, unique=True, null=True)
    message = models.CharField(max_length=100, null=True)
