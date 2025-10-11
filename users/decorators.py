from django.http import HttpResponseForbidden
from .models import User


# 커스텀 데코레이터 생성 (이 User이 소유권이 필요하다)
def account_ownership_required(func):
    def decorated(request, *args, **kwargs):
        # 요청을 받으면서 primary key로 받은 그 값을 가지고 있는 User.object를 user 변수에 대입
        user = User.objects.get(pk=kwargs["pk"])
        if not user == request.user:
            return HttpResponseForbidden()
        return func(request, *args, **kwargs)

    return decorated
