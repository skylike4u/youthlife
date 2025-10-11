from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = "core/home.html"

    # 장고문서 예시)
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["latest_articles"] = Article.objects.all()[:5]
    #     return context
