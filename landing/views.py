from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView, RedirectView, TemplateView

from unfold.views import UnfoldModelAdminViewMixin

from landing.forms import CustomForm


class HomeView(TemplateView):
    template_name = "index.html"


class BookView(TemplateView):
    template_name = "booking.html"
    success_url = reverse_lazy("booking:result")


class ResultView(TemplateView):
    template_name = "result.html"


class CrispyFormView(FormView):
    title = "Бронирование"
    form_class = CustomForm
    success_url = reverse_lazy("booking:result")
    template_name = "booking_crispy_form.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
