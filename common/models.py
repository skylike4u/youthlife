from django.db import models


# 다른 애플리케이션들과 공유할 수 있는 공통 코드를 가지고 있는 앱 / 예를 들어 내 애플리케이션의 모든 model이 created_At과 updated_at을 가졌으면 할때 /
# 이 model은 데이터베이스에 추가하지 않을 model (재사용 model / 설계도 blueprint)
class CommonModel(models.Model):
    """Common model Definition"""

    # 처음 만들때 생성
    created_at = models.DateTimeField(auto_now_add=True)
    # 업데이트 할 때마다 설정
    updated_at = models.DateTimeField(auto_now=True)

    # 이 문구 사용하면 Django가 이 model을 봐도 이걸 데이터베이스에 저장하지 않음
    # abstract응 니 model이 데이터베이스에서 실제 데이터로 사용되지 않을거란 뜻
    class Meta:
        abstract = True
