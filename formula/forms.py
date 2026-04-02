from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Div, Fieldset, Layout, Row
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.views.generic import RedirectView
from unfold.forms import AuthenticationForm
from unfold.layout import Submit
from unfold.widgets import (
    UnfoldAdminCheckboxSelectMultiple,
    UnfoldAdminDateWidget,
    UnfoldAdminEmailInputWidget,
    UnfoldAdminExpandableTextareaWidget,
    UnfoldAdminFileFieldWidget,
    UnfoldAdminImageFieldWidget,
    UnfoldAdminIntegerFieldWidget,
    UnfoldAdminMoneyWidget,
    UnfoldAdminRadioSelectWidget,
    UnfoldAdminSelect2Widget,
    UnfoldAdminSelectWidget,
    UnfoldAdminNullBooleanSelectWidget,
    UnfoldAdminSelectMultipleWidget,
    UnfoldAdminSplitDateTimeWidget,
    UnfoldAdminTextareaWidget,
    UnfoldAdminTextInputWidget,
    UnfoldAdminTimeWidget,
    UnfoldAdminURLInputWidget,
    UnfoldBooleanSwitchWidget,
    UnfoldBooleanWidget,
)

from formula.models import Booking, Room


class HomeView(RedirectView):
    pattern_name = "admin:index"


class RoomFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.template = "unfold_crispy/layout/table_inline_formset.html"
        self.form_id = "room-formset"
        self.form_add = True
        self.form_show_labels = False
        self.attrs = {
            "novalidate": "novalidate",
        }
        self.add_input(Submit("submit", "Сохранить"))


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = [
            "name",
            "category",
            "price_per_day",
            "is_active",
            "is_available"
        ]
        widgets = {
            "name": UnfoldAdminTextInputWidget(),
            "category": UnfoldAdminSelectWidget(),
            "price_per_day": UnfoldAdminMoneyWidget(),
            "is_active": UnfoldAdminNullBooleanSelectWidget(),
            "is_available": UnfoldAdminNullBooleanSelectWidget(),
        }

    def clean(self):
        raise ValidationError("Testing form wide error messages.")


class RoomFormSet(forms.BaseModelFormSet):
    def clean(self):
        raise ValidationError("Testing formset wide error messages.")


class LoginForm(AuthenticationForm):
    password = forms.CharField(widget=forms.PasswordInput(render_value=True))

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)

        if settings.LOGIN_USERNAME and settings.LOGIN_PASSWORD:
            self.fields["username"].initial = settings.LOGIN_USERNAME
            self.fields["password"].initial = settings.LOGIN_PASSWORD
