from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
    FormView,
)
from django.views.generic.list import MultipleObjectMixin
from django.contrib.auth.forms import UserCreationForm
from .models import User
from . import models, forms

from users.decorators import account_ownership_required

from articles.models import Article

has_ownership = [account_ownership_required, login_required]


# CreateView를 이용한 회원가입(Sign up)
class UserCreateView(CreateView):
    # custumizing User를 사용
    model = User
    # 장고의 기본제공 UserCreationForm 사용(확인필요: 커스터마이징 해야되지 않나??)
    form_class = UserCreationForm
    success_url = reverse_lazy("core:home")
    template_name = "users/create_user.html"


# 특정유저의 정보를 봐야됨(계정의 ID(primary key)가 필요)
class UserDetailView(DeleteView):
    """개별User의 DetailView 페이지 생성"""

    model = User
    context_object_name = "target_user"
    template_name = "users/detail.html"

    paginate_by = 25

    def get_context_data(self, **kwargs):
        object_list = Article.objects.filter(writer=self.get_object())
        return super(UserDetailView, self).get_context_data(
            object_list=object_list, **kwargs
        )


# @method_decorator() -> 일반 function (def)에 사용하는 decorator를 특정class의 method에 사용할 수 있도록 변환해주는 데코레이터임
# @method_decorator(login_required, "get")
# @method_decorator(login_required, "post")
# @method_decorator(account_ownership_required, "get")
# @method_decorator(account_ownership_required, "post")
## 배열(list)로 메소드_데코레이터 안에 하나(has_ownership)만 넣어주면은 이 배열 내에 있는 데코레이터들을 모두 확인하고 체크를 해줍니다.
@method_decorator(has_ownership, "get")
@method_decorator(has_ownership, "post")
class UserUpdateView(UpdateView):
    # 장고의 기본제공 User를 사용
    model = User
    context_object_name = "target_user"
    # 기본제공 UserCreationForm은 ID 변경가능 문제가 있어, 상속받아 별도 커스터마이징한 form을 불러옴
    form_class = forms.AccountUpdateForm
    success_url = reverse_lazy("users:update")
    template_name = "users/update.html"


# 데코레이터 사용 전 버전 (기본적으로 이렇게 작성할 것!!!(아래)
# class AccountUpdateView(UpdateView):
#     # 장고의 기본제공 User를 사용
#     model = User
#     context_object_name = 'target_user'
#     # 기본제공 UserCreationForm은 ID 변경가능 문제가 있어, 상속받아 별도 커스터마이징한 form을 불러옴
#     form_class = forms.AccountUpdateForm
#     success_url = reverse_lazy("accountapp:home")
#     template_name = "accountapp/update.html"

#     # 로그인이 안된 사람은 볼 수 없도록, get 및 post 메소드 모두 인증처리
#     # self는 현재 해당 class 자체(AccountUpdateView)를 가르킴.
#     # 이 안에서 get_object는 현재 사용되고 있는 pk에 해당하는 user객체(object)를 가져옴. 지금 request를 보내고 있는 user와 같은지 확인
#     def get(self, *args, **kwargs):
#         if self.request.user.is_authenticated and self.get_object() == self.request.user:
#             return super().get(*args, **kwargs)
#         else:
#             return HttpResponseForbidden()
#     def post(self, *args, **kwargs):
#         if self.request.user.is_authenticated and self.get_object() == self.request.user:
#             return super().post(*args, **kwargs)
#         else:
#             return HttpResponseForbidden()


# @method_decorator(login_required, "get")
# @method_decorator(login_required, "post")
# @method_decorator(account_ownership_required, "get")
# @method_decorator(account_ownership_required, "post")
@method_decorator(has_ownership, "get")
@method_decorator(has_ownership, "post")
class UserDeleteView(DeleteView):
    model = User
    context_object_name = "target_user"
    success_url = reverse_lazy("users:login")
    template_name = "users/delete.html"

    # 로그인이 안된 사람은 볼수 없도록, get 및 post 메소드 모두 인증처리
    def get(self, *args, **kwargs):
        if (
            self.request.user.is_authenticated
            and self.get_object() == self.request.user
        ):
            return super().get(*args, **kwargs)
        else:
            # 금지되어 있는 곳에 접근해있다는 것을 보여줌
            return HttpResponseForbidden()

    def post(self, *args, **kwargs):
        if (
            self.request.user.is_authenticated
            and self.get_object() == self.request.user
        ):
            return super().post(*args, **kwargs)
        else:
            return HttpResponseForbidden()


# login_required 데코레이터 미사용 버전(아래)
# def hello_world(request):

#     # 여기에 인증을 넣어줄거야(사용자가 로그인했으면 정상적으로 할수 있지만 아닌경우에는 로그인창으로 되돌려보냄)
#     # request 안에 user라는 객체(object)가 있음. 그 안에 is_authenticated라는 메소드가 있음
#         # nav에서 user.is_authenficated가 user가 로그인했는지 아닌지 확인할 수 있는 방법이었는데, views.py에서도 똑같이 사용할 수 있음
#     if request.user.is_authenticated:
#         """form 입력에 대해 post방식의 전송 및 저장, get방식 예외처리"""
#         if request.method == "POST":
#             temp = request.POST.get("hello_world_input")

#             # Member 인스턴스 생성하여 변수대입
#             new_hello_world = models.Member()
#             new_hello_world.member_list = temp
#             new_hello_world.save()

#             # new_member_list = models.Member.objects.all()

#             # HttpResponseRedirect: 다른 페이지로 redirect할 때 사용 ex) form POST전송 성공 이후
#             return HttpResponseRedirect(reverse("accountapp:home"))
#         # method가 get일때
#         else:
#             new_member_list = models.Member.objects.all()
#             return render(request, "accountapp/hello_world.html", context={"new_member_list": new_member_list})
#     # 로그인이 안되어 있으면(else) 로그인창으로 되돌려 보내줌
#     else:
#         return HttpResponseRedirect(reverse('accountapp:login'))
