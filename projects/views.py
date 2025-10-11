from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, DetailView
from django.views.generic.list import MultipleObjectMixin
from django.urls import reverse, reverse_lazy

from projects.forms import ProjectCreationForm
from projects.models import Project
from articles.models import Article


@method_decorator(login_required, "get")
@method_decorator(login_required, "post")
class ProjectCreateView(CreateView):
    """Project CreateView Definition"""

    model = Project
    form_class = ProjectCreationForm
    template_name = "projects/create.html"

    # 끝나고 나서 어디로 url로 향하는지 설정
    def get_success_url(self):
        return reverse("projects:detail", kwargs={"pk": self.object.pk})


class ProjectListView(ListView):
    """Project List View"""

    model = Project
    context_object_name = "project_list"
    paginate_by = 25
    template_name = "projects/list.html"


class ProjectDetailView(DetailView, MultipleObjectMixin):
    """Project Detail View"""

    model = Project
    context_object_name = "target_project"
    template_name = "projects/detail.html"

    paginate_by = 25

    def get_context_data(self, **kwargs):
        object_list = Article.objects.filter(project=self.get_object())
        return super(ProjectDetailView, self).get_context_data(
            object_list=object_list, **kwargs
        )

    """ (구독기능포함 -완성본)
    # get_context_list 메소드를 사용해서 필터링
    # 템플릿 창에서 object_list라는 것을 사용해서 필터링한 게시글(self가 작성한 article)들을 사용할 수 있음
    def get_context_data(self, **kwargs):
        project = self.object
        user = self.request.user

        if user.is_authenticated:
            subscription = Subscription.objects.filter(user=user, project=project)
        else:
            subscription = None
        # template에서 subscription을 통해서 구독정보가 있는 지 여부를 확인할 수 있음
        # project라는 값이 self.get_object()와 같은 값을 가진 article을 모두 필터링해서, object_list 변수 안에 넣는다
        # 템플릿 창에서 object_list라는 것을 사용해서, 필터링한 게시글들을 사용할 수 있게 된다.
        object_list = Article.objects.filter(project=self.get_object())
        return super(ProjectDetailView, self).get_context_data(
            object_list=object_list, subscription=subscription, **kwargs
        ) """
