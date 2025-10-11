from django.http import HttpResponseForbidden

from profiles.models import Profile


# 커스텀 데코레이터 생성 (이 profile에 소유권이 필요하다)
def profile_ownership_required(func):
    def decorated(request, *args, **kwargs):
        # 요청을 받으면서 primary key로 받은 그 값을 가지고 있는 Profile.objects를 profile 변수에 대입
        profile = Profile.objects.get(pk=kwargs["pk"])
        if not profile.user == request.user:
            return HttpResponseForbidden()
        return func(request, *args, **kwargs)

    return decorated
