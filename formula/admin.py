import json
import random

from django import forms
from django.contrib import admin, messages
from django.core.validators import EMPTY_VALUES
from django.db.models import OuterRef, Q, Sum
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import path, reverse_lazy
from django.utils.translation import gettext_lazy as _

from djangoql.admin import DjangoQLSearchMixin
from guardian.admin import GuardedModelAdmin
from import_export.admin import ExportActionModelAdmin, ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin
from unfold.admin import (
    GenericStackedInline,
    ModelAdmin,
    StackedInline,
    TabularInline,
)
from unfold.components import BaseComponent, register_component
from unfold.contrib.filters.admin import (
    AllValuesCheckboxFilter,
    AutocompleteSelectMultipleFilter,
    BooleanRadioFilter,
    CheckboxFilter,
    ChoicesCheckboxFilter,
    RangeDateFilter,
    RangeNumericFilter,
    RelatedCheckboxFilter,
    RelatedDropdownFilter,
    SingleNumericFilter,
    SliderNumericFilter,
    TextFilter,
)
from unfold.contrib.forms.widgets import WysiwygWidget
from unfold.contrib.import_export.forms import (
    ExportForm,
    ImportForm,
    SelectableFieldsExportForm,
)
from unfold.contrib.inlines.admin import NonrelatedStackedInline
from unfold.datasets import BaseDataset
from unfold.decorators import action, display
from unfold.enums import ActionVariant
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.paginator import InfinitePaginator
from unfold.sections import TableSection, TemplateSection
from unfold.widgets import (
    UnfoldAdminCheckboxSelectMultiple,
    UnfoldAdminSelect2Widget,
    UnfoldAdminSelectWidget,
    UnfoldAdminSplitDateTimeWidget,
    UnfoldAdminTextInputWidget,
)

from formula.models import (
    Room,
    Booking,
    ActivityCategory,
)

from formula.views import CrispyFormsetView


class RoomNonrelatedStackedInline(NonrelatedStackedInline):
    model = Room
    fields = ["name", "category", "price_per_day"]
    extra = 1
    tab = True
    per_page = 10

    def get_form_queryset(self, obj):
        return self.model.objects.all().distinct()

    def save_new_instance(self, parent, instance):
        pass


# class UserDriverTabularInline(TabularInline):
#     model = Driver
#     fk_name = "editor"
#     # autocomplete_fields = ["standing"]
#     fields = ["first_name", "last_name", "code", "status", "salary", "category"]


# class DriverTableSection(TableSection):
#     related_name = "race_set"
#     fields = ["winner", "laps", "date"]


# class CircuitRaceInline(TabularInline):
#     model = Race
#     autocomplete_fields = ["winner"]
#     fields = ["winner", "year", "laps", "date"]
#     ordering_field = "weight"
#     extra = 0
#     show_change_link = True


class FullNameFilter(TextFilter):
    title = "Полное имя"
    parameter_name = "fullname"

    def queryset(self, request, queryset):
        if self.value() in EMPTY_VALUES:
            return queryset

        return queryset.filter(
            Q(first_name__icontains=self.value()) | Q(last_name__icontains=self.value())
        )


# class RaceWinnerInline(StackedInline):
#     model = Race
#     fields = ["winner", "year", "laps", "picture"]
#     readonly_fields = ["winner", "year", "laps"]
#     ordering_field = "weight"
#     extra = 0
#     per_page = 15
#     tab = True


class ChartSection(TemplateSection):
    template_name = "formula/client_section.html"


class PreferedBudgetSliderNumericFilter(SliderNumericFilter):
    MAX_DECIMALS = 2


@admin.register(Room)
class RoomAdmin(ModelAdmin, ImportExportModelAdmin, ExportActionModelAdmin):
    show_facets = False
    search_fields = ["name", "description"]
    list_display = ["name", "category", "price_per_day", "is_active", "is_available"]
    list_filter = ["category", "is_active", "is_available"]
    # inlines = [CircuitRaceInline]
    ordering_field = "name"
    hide_ordering_field = True
    compressed_fields = True

    # list_sections = [DriverTableSection] # hihi
    save_as = True
    import_form_class = ImportForm
    export_form_class = ExportForm
    export_form_class = SelectableFieldsExportForm

    actions_detail = ["custom_actions_detail"]
    actions_submit_line = ["custom_actions_submit_line"]

    def get_urls(self):
        return super().get_urls() + [
            path(
                "crispy-with-formset",
                self.admin_site.admin_view(CrispyFormsetView.as_view(model_admin=self)),
                name="crispy_formset",
            ),
        ]

    @action(
        description="Custom detail action",
        url_path="actions-detail-custom-url",
        permissions=["custom_actions_detail"],
    )
    def custom_actions_detail(self, request, object_id):
        messages.success(
            request,
            f"Detail action has been successfully executed. Object ID {object_id}",
        )
        return redirect(request.headers["referer"])

    def has_custom_actions_detail_permission(self, request, object_id):
        return request.user.is_superuser or request.user.is_staff


    @action(
        description="Custom submit line action",
        permissions=[
            "custom_actions_submit_line",
        ],
    )
    def custom_actions_submit_line(self, request, obj):
        messages.success(
            request,
            f"Detail action has been successfully executed. Object ID {obj.pk}",
        )

    def has_custom_actions_submit_line_permission(self, request, obj):
        return request.user.is_superuser


@admin.register(Booking)
class BookingAdmin(GuardedModelAdmin, SimpleHistoryAdmin, DjangoQLSearchMixin, ModelAdmin):
    fieldsets = [
        (
            "Клиент",
            {
                "fields": [
                    "first_name",
                    "last_name",
                    "middle_name",
                    "description",
                    "age",
                ]
            },
        ),
        (
            "Заявка",
            {
                "classes": ["tab"],
                "fields": [
                    "room",
                    "preferred_check_in",
                    "preferred_budget"
                ],
            },
        ),
        (
            "Контакты",
            {
                "classes": ["tab"],
                "fields": [
                    "phone",
                    "preferred_call_time",
                ],
            },
        ),
        (
            "Статус", 
            {
                "fields": [
                    "status"
                ]
            }
        )
    ]

    list_display = [
        "display_client",
        "age",
        "display_details",
        "preferred_check_in",
        "display_contacts",
        "status",
        "modified_at",
    ]

    list_filter = [
        FullNameFilter,
        ("age", RangeNumericFilter),
        ("created_at", RangeDateFilter),
        ("preferred_check_in", RangeDateFilter),
        ("preferred_budget", PreferedBudgetSliderNumericFilter),
        ("room", RelatedDropdownFilter),
    ]
    list_filter_sheet = False
    list_filter_submit = False
    
    list_fullwidth = True
    list_horizontal_scrollbar_top = True
    list_select_related = ['room']

    list_sections = [ChartSection]
    list_sections_classes = "lg:grid-cols-2"

    # raw_id_fields = ["room"]
    # form = ClientAdminForm

    history_list_per_page = 10

    search_fields = ["last_name", "first_name", "description"]

    warn_unsaved_form = True
    compressed_fields = True

    # inlines = [RaceWinnerInline]
    
    autocomplete_fields = []

    radio_fields = {
        "status": admin.VERTICAL,
    }

    readonly_fields = []

    actions_list = []
    actions_detail = ["archive"]

    change_form_show_cancel_button = True

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        form.base_fields["first_name"].widget = UnfoldAdminTextInputWidget(
            attrs={
                "class": "first-name-input",
            }
        )
        return form

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .prefetch_related(
                "room",
            )
        )
    
    @display(
        description="Клиент",
    )
    def display_client(self, instance: Booking):
        return instance.full_name


    @display(
        description="Детали",
    )
    def display_details(self, instance: Booking):
        if instance.room:
            return f'Комната "{instance.room}"'
        return f'Комната не выбрана (бюджет {instance.preferred_budget})'


    @display(
        description="Контактные данные",
    )
    def display_contacts(self, instance: Booking):
        if instance.preferred_call_time:
            return f'{instance.phone} ({instance.preferred_call_time.time})' 
        return instance.phone


    @action(description="Отправить в архив", permissions=["archive"])
    def archive(self, request, object_id):
        messages.success(
            request, "Заявка была отклонена и отправлена в архив"
        )
        return redirect(reverse_lazy("admin:formula_booking_change", args=[object_id]))

    def has_archive_permission(self, request, object_id):
        return request.user.is_superuser


@register_component
class BookingActiveComponent(BaseComponent):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["children"] = render_to_string(
            "formula/helpers/kpi_progress.html",
            {
                "total": Booking.objects.filter(room__category=ActivityCategory.STANDARD).count(),
                "progress": "positive",
                "percentage": "2.8%",
            },
        )
        return context


@register_component
class BookingInactiveComponent(BaseComponent):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["children"] = render_to_string(
            "formula/helpers/kpi_progress.html",
            {
                "total": Booking.objects.filter(room__category=ActivityCategory.BEDRIDDEN).count(),
                "progress": "negative",
                "percentage": "-12.8%",
            },
        )
        return context


@register_component
class DriverTotalPointsComponent(BaseComponent):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["children"] = render_to_string(
            "formula/helpers/kpi_progress.html",
            {
                "progress": "positive",
                "percentage": "24.2%",
            },
        )
        return context


@register_component
class ClientBookingsComponent(BaseComponent):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["children"] = render_to_string(
            "formula/helpers/kpi_progress.html",
            {
                "total": Booking.objects.count(),
                "progress": "negative",
                "percentage": "-10.0%",
            },
        )
        return context


@register_component
class BookingSectionChangeComponent(BaseComponent):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        WEEKDAYS = [
            "Mon",
            "Tue",
            "Wed",
            "Thu",
            "Fri",
            "Sat",
            "Sun",
        ]
        OF_DAYS = 21

        context["data"] = json.dumps(
            {
                "labels": [WEEKDAYS[day % 7] for day in range(1, OF_DAYS)],
                "datasets": [
                    {
                        "data": [
                            [1, random.randrange(8, OF_DAYS)] for i in range(1, OF_DAYS)
                        ],
                        "backgroundColor": "var(--color-primary-600)",
                    }
                ],
            }
        )
        return context
