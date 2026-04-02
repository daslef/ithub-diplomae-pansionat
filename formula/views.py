from django.contrib import messages
from django.forms import modelformset_factory
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView, RedirectView, TemplateView
from unfold.views import UnfoldModelAdminViewMixin

from formula.forms import (
    RoomForm,
    RoomFormHelper,
    RoomFormSet,
)

from formula.models import Booking, Room




class CrispyFormsetView(UnfoldModelAdminViewMixin, FormView):
    title = "Редактирование"
    success_url = reverse_lazy("admin:crispy_formset")
    permission_required = (
        "formula.view_room",
        "formula.add_room",
        "formula.change_room",
        "formula.delete_room",
    )
    template_name = "formula/room_crispy_formset.html"

    def get_form_class(self):
        return modelformset_factory(
            Room, RoomForm, formset=RoomFormSet, extra=1, can_delete=True
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # kwargs.update(
        #     {
        #         "queryset": Driver.objects.filter(code__in=["VER", "HAM"]),
        #     }
        # )
        return kwargs

    def form_invalid(self, form):
        messages.error(self.request, _("Formset submitted with errors"))
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, _("Formset submitted successfully"))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(
            {
                "room_formset_helper": RoomFormHelper(),
            }
        )
        return context
