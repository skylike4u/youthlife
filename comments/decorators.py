from django.http import HttpResponseForbidden

from comments.models import Comment


# comment의 주인인지 아닌지 확인하는 과정이 필요해서 데코레이터 사용
# 커스텀 데코레이터 생성 (이 profile에 소유권이 필요하다)
def comment_ownership_required(func):
    def decorated(request, *args, **kwargs):
        # 요청을 받으면서 primary key로 받은 그 값을 가지고 있는 article.objects를 article 변수에 대입
        # pk에 해당하는 article을 찾아서 변수 대입
        comment = Comment.objects.get(pk=kwargs["pk"])
        if not comment.writer == request.user:
            # article의 writer가 지금의 request를 보내는 user와 같은지를 확인하고 아니라면 금지되었다고 말해줌
            return HttpResponseForbidden()
        return func(request, *args, **kwargs)

    return decorated
