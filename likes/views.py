from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import RedirectView
from django.http import HttpResponseRedirect

from articles.models import Article
from likes.models import Like


@transaction.atomic
def db_transaction(user, article):

    article.like += 1
    article.save()

    # like record가 존재할때는 에러를 발생시킴
    if Like.objects.filter(user=user, article=article).exists():
        raise ValidationError("Like already exists")
    else:
        Like(user=user, article=article).save()


# 로그인이 안되어 있으면 로그인 창으로 가도록 설정
@method_decorator(login_required, "get")
class LikeArticleView(RedirectView):
    # get_redirect_url을 오버라이딩해서 우리가 원하는데로 redirect하도록 만듦
    def get_redirect_url(self, *args, **kwargs):
        # 요청받는 게시글로 재연결하도록 설정을 해줌 (like버튼 클릭하면 해당페이지에 그대로 머무름)
        return reverse("articles:detail", kwargs={"pk": kwargs["pk"]})

    def get(self, *args, **kwargs):

        # 여기에 우리가 원하는 알고리즘을 넣어 줘야 함
        # user랑 aritcle을 특정시켜줌 (request를 보내는 유저 / article은 article 안에서 pk를 받은 그 aricle임)
        # pk가 있는 article을 가져오고 아니면 404에러를 발생시켜라
        user = self.request.user
        article = get_object_or_404(Article, pk=kwargs["pk"])

        try:
            db_transaction(user, article)
            messages.add_message(
                self.request, messages.SUCCESS, "좋아요가 반영되었습니다."
            )
        except ValidationError:
            messages.add_message(
                self.request, messages.ERROR, "좋아요는 한번만 가능합니다."
            )
            return HttpResponseRedirect(
                reverse("articles:detail", kwargs={"pk": kwargs["pk"]})
            )

        return super(LikeArticleView, self).get(self.request, *args, **kwargs)
