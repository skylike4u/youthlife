from django.http import HttpResponseForbidden

from blogs.models import Post


# 해당 post의 주인인지 아닌지 확인하는 과정이 필요해서 데코레이터로 사용
# 커스텀 데코레이터 생성 (이 post에 소유권이 필요하다)
def post_ownership_required(func):
    def decorated(request, *args, **kwargs):
        # 요청을 받으면서 primary key로 받은 그 값을 가지고 있는 post.objects를 post 변수에 대입
        # pk에 해당하는 post을 찾아서 변수 대입
        post = Post.objects.get(pk=kwargs["pk"])
        if not post.writer == request.user:
            # post의 writer가 지금의 request를 보내는 user와 같은지를 확인하고 아니라면 금지되었다고 말해줌
            return HttpResponseForbidden()
        return func(request, *args, **kwargs)

    return decorated
