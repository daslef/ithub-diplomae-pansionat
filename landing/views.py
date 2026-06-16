from django.urls import reverse_lazy
from django.views.generic import FormView, RedirectView, TemplateView

from landing.forms import CustomForm


class HomeView(TemplateView):
    template_name = "index.html"


class BookView(FormView, TemplateView):
    title = "Бронирование"
    template_name = "booking_crispy_form.html"
    form_class = CustomForm
    success_url = reverse_lazy("result")

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class ResultView(TemplateView):
    template_name = "result.html"
