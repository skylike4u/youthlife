from django.views.generic import CreateView, UpdateView
from django.shortcuts import render
from django.urls import reverse_lazy, reverse

from profiles.decorators import profile_ownership_required
from django.utils.decorators import method_decorator


from profiles.models import Profile
from profiles.forms import ProfileCreationForm


class ProfileCreateView(CreateView):
    model = Profile
    context_object_name = "target_profile"
    form_class = ProfileCreationForm
    template_name = "profiles/create.html"

    # user data 추가 (modelform으로 user 데이터를 바로 집어넣으면 다른사람들이 profile 수정할수 있어서, user를 빼고 form_valid 메소드로 커스터마이징함)
    def form_valid(self, form):
        # form에서 날라온 데이터를 임시 저장(DB반영 X)
        temp_profile = form.save(commit=False)
        # user데이터 추가
        temp_profile.user = self.request.user
        temp_profile.save()
        # 원래 조상 form_valid 리턴
        return super().form_valid(form)

    # detail 페이지의 user pk를 넘겨주기 위해 오버라이딩
    # update되면 정상적으로 user의 디테일페이지로 redirect되는 것으로 만드는 작업

    # sucess_url 파라미터를 안쓰는 이유(아래)는 pk를 넣어 줄수 없기 때문에, 아래처럼 get_success_url 메소드를 사용(내부 메소드 수정)해서 pk데이터도 함께 전달해준다
    # sucess_url = reverse_lazy('users:detail') 만으로는 추가적인 pk지정이 안됨
    # get_success_url을 통해 동적인 redirect url을 반환해 주도록 변경 (동적 pk 전달)
    def get_success_url(self):
        # 아래 self.object가 가르키는 것은 "profile"(model 지정)이고, profile의 user의 pk를 찾아서 같이 데이터를 넘겨줌
        return reverse("users:detail", kwargs={"pk": self.object.user.pk})


# 보안사항을 기본적으로 생성
@method_decorator(profile_ownership_required, "get")
@method_decorator(profile_ownership_required, "post")
class ProfileUpdateView(UpdateView):
    """Profile View update"""

    model = Profile
    context_object_name = "target_profile"
    form_class = ProfileCreationForm
    template_name = "profiles/update.html"

    def get_success_url(self):
        # 아래 self.object가 가르키는 것은 profile(model 지정)이고, profile의 user의 pk를 찾아서 같이 데이터를 넘겨줌
        return reverse("users:detail", kwargs={"pk": self.object.user.pk})
