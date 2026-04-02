from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Div, Fieldset, Layout, Row

from unfold.layout import Submit
from unfold.widgets import (
    UnfoldAdminIntegerFieldWidget,
    UnfoldAdminMoneyWidget,
    UnfoldAdminSelect2Widget,
    UnfoldAdminNullBooleanSelectWidget,
    UnfoldAdminSplitDateTimeWidget,
    UnfoldAdminTextareaWidget,
    UnfoldAdminTextInputWidget,
    UnfoldAdminTimeWidget,
    UnfoldBooleanSwitchWidget,
    UnfoldBooleanWidget,
)


class CustomFormMixin(forms.Form):
    first_name = forms.CharField(
        max_length=30,
        label="Имя",
        required=True,
        widget=UnfoldAdminTextInputWidget(),
    )

    last_name = forms.CharField(
        max_length=30,
        label="Фамилия",
        required=True,
        widget=UnfoldAdminTextInputWidget(),
    )

    middle_name = forms.CharField(
        max_length=30,
        label="Отчество",
        required=False,
        widget=UnfoldAdminTextInputWidget(),
    )

    age = forms.IntegerField(
        label="Возраст",
        required=True,
        min_value=18,
        max_value=120,
        widget=UnfoldAdminIntegerFieldWidget(),
    )

    phone = forms.CharField(
        max_length=30,
        label="Телефон",
        required=True,
        widget=UnfoldAdminTextInputWidget(),
    )

    preferred_call_time = forms.TimeField(
        label="Удобное время для звонка",
        required=False,
        widget=UnfoldAdminTimeWidget,
    )

    agreement = forms.BooleanField(
        label="Согласен на обработку данных",
        required=True,
        initial=False,
        help_text="Для передачи заявки необходимо ознакомиться и принять условия соглашения",
        widget=UnfoldBooleanWidget,
    )

    preferred_budget = forms.DecimalField(
        label="Предпочтительный бюджет",
        required=True,
        help_text="Укажите желаемую стоимость/день, и мы поможем подобрать комнату",
        widget=UnfoldAdminMoneyWidget,
    )

    preferred_check_in = forms.SplitDateTimeField(
        label="Дата заселения",
        required=False,
        help_text="Укажите желаемую дату заселения, если уже определились",
        widget=UnfoldAdminSplitDateTimeWidget,
    )

    description = forms.CharField(
        label="Описание",
        required=True,
        widget=UnfoldAdminTextareaWidget(),
    )
    
    room = forms.TypedChoiceField(
        label="Комната",
        choices=[
            (1, "Low"),
            (2, "Medium"),
            (3, "High"),
        ],
        coerce=int,
        required=False,
        help_text="Выберите желаемые комнаты",
        widget=UnfoldAdminSelect2Widget,
    )



class CustomForm(CustomFormMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", "Отправить заявку", css_class="text-black bg-green-700"))
        self.helper.attrs = {
            "novalidate": "novalidate",
        }
        self.helper.layout = Layout(
            Column(
                Fieldset(
                    "Форма бронирования",
                    Row(
                        Div("last_name", css_class="flex-1"),
                        "first_name",
                        "middle_name",
                        "age",
                        css_class="w-full flex"
                    ),
                    "description",
                    "preferred_check_in",
                    Row(
                        "phone",
                        "preferred_call_time",
                        css_class="gap-5",
                    ),
                ),
                Fieldset(
                    "Комната",
                    Div("room"),
                    Div("preferred_budget"),
                ),
                Row(
                    Div("agreement", css_class="w-2/3"),
                ),
                css_class="gap-5"
            )
        )

