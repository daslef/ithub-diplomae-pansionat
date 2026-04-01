import json
import random

from django import forms
from django.contrib import admin, messages
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.core.validators import EMPTY_VALUES
from django.db import models
from django.db.models import OuterRef, Q, Sum
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.templatetags.static import static
from django.urls import path, reverse_lazy
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from djangoql.admin import DjangoQLSearchMixin
from guardian.admin import GuardedModelAdmin
from import_export.admin import ExportActionModelAdmin, ImportExportModelAdmin
from modeltranslation.admin import TabbedTranslationAdmin
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
    RangeDateTimeFilter,
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
    Client,
    Booking,
    BookingWithFilters,
    ActivityCategory,
    Profile,
    User,
)

from formula.resources import RoomResource, AnotherRoomResource
from formula.views import CrispyFormsetView, CrispyFormView

admin.site.unregister(Group)


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


class UserProfileTabularInline(TabularInline):
    model = Profile
    fields = ["user", "picture", "resume", "link"]


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_fullwidth = True
    list_filter = [
        ("is_staff", BooleanRadioFilter),
        ("is_superuser", BooleanRadioFilter),
        ("is_active", BooleanRadioFilter),
        ("groups", RelatedCheckboxFilter),
    ]
    list_filter_submit = True
    list_filter_sheet = False
    change_form_datasets = []
    inlines = [
        RoomNonrelatedStackedInline,
        # UserDriverTabularInline,
        UserProfileTabularInline,
    ]
    compressed_fields = True
    list_display = [
        "display_header",
        "is_active",
        "display_staff",
        "display_superuser",
        "display_created",
    ]
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Личная информация",
            {
                "fields": (("first_name", "last_name"), "email", "biography"),
                "classes": ["tab"],
            },
        ),
        (
            "Права",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
                "classes": ["tab"],
            },
        ),
        (
            "Даты",
            {
                "fields": ("last_login", "date_joined"),
                "classes": ["tab"],
            },
        ),
    )
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        }
    }
    readonly_fields = ["last_login", "date_joined"]
    show_full_result_count = False

    @display(description=_("User"))
    def display_header(self, instance: User):
        return instance.username

    @display(description=_("Staff"), boolean=True)
    def display_staff(self, instance: User):
        return instance.is_staff

    @display(description=_("Superuser"), boolean=True)
    def display_superuser(self, instance: User):
        return instance.is_superuser

    @display(description=_("Created"))
    def display_created(self, instance: User):
        return instance.created_at


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        return super().changelist_view(request, extra_context=extra_context)


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
    resource_classes = [RoomResource, AnotherRoomResource]
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
        permissions=["custom_actions_detail", "another_custom_actions_detail"],
    )
    def custom_actions_detail(self, request, object_id):
        messages.success(
            request,
            f"Detail action has been successfully executed. Object ID {object_id}",
        )
        return redirect(request.headers["referer"])

    def has_custom_actions_detail_permission(self, request, object_id):
        return request.user.is_superuser

    def has_another_custom_actions_detail_permission(self, request, object_id):
        return request.user.is_staff

    @action(
        description="Custom submit line action",
        permissions=[
            "custom_actions_submit_line",
            "another_custom_actions_submit_line",
        ],
    )
    def custom_actions_submit_line(self, request, obj):
        messages.success(
            request,
            f"Detail action has been successfully executed. Object ID {obj.pk}",
        )

    def has_custom_actions_submit_line_permission(self, request, obj):
        return request.user.is_superuser

    def has_another_custom_actions_submit_line_permission(self, request, obj):
        return request.user.is_staff


class FullNameFilter(TextFilter):
    title = _("full name")
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


class ClientAdminForm(forms.ModelForm):
    # flags = forms.MultipleChoiceField(
    #     label=_("Flags"),
    #     choices=[
    #         ("POPULAR", _("Popular")),
    #         ("FASTEST", _("Fastest")),
    #         ("TALENTED", _("Talented")),
    #     ],
    #     required=False,
    #     widget=UnfoldAdminCheckboxSelectMultiple,
    # )
    first_name = forms.CharField(
        label=_("First name"),
        widget=UnfoldAdminTextInputWidget,
    )
    custom_text_input = forms.CharField(
        label=_("Custom Text Input"),
        required=False,
        widget=UnfoldAdminTextInputWidget,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["first_name"].widget.attrs.update(
            {
                "prefix_icon": "search",
                "suffix_icon": "euro",
            }
        )


class ChartSection(TemplateSection):
    template_name = "formula/client_section.html"


class ClientAdminMixin(DjangoQLSearchMixin, ModelAdmin):
    list_horizontal_scrollbar_top = True
    list_sections = [ChartSection]
    # list_sections_classes = "lg:grid-cols-2"
    form = ClientAdminForm
    history_list_per_page = 10
    search_fields = ["last_name", "first_name"]
    warn_unsaved_form = True
    compressed_fields = True
    list_display = [
        "display_description",
        "display_category",
        # "is_active",
    ]
    actions_row = [
        "custom_actions_row",
        "custom_actions_row2",
    ]

    # inlines = [RaceWinnerInline]
    
    # autocomplete_fields = [
    #     "editor",
    # ]
    # radio_fields = {
    #     "status": admin.VERTICAL,
    # }
    readonly_fields = [
        # "picture",
        # "resume",
    ]
    list_before_template = "formula/driver_list_before.html"
    change_form_show_cancel_button = True
    change_form_before_template = "formula/driver_change_form_before.html"
    change_form_after_template = "formula/driver_change_form_after.html"

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        form.base_fields["first_name"].widget = UnfoldAdminTextInputWidget(
            attrs={
                "class": "first-name-input",
            }
        )
        return form

    # def get_queryset(self, request):
    #     return (
    #         super()
    #         .get_queryset(request)
    #         .prefetch_related(
    #             "race_set",
    #             "race_set__circuit",
    #         )
    #     )

    @display(
        description="Категория",
        label={
            ActivityCategory.BEDRIDDEN: "danger",
            ActivityCategory.STANDARD: "success",
        },
    )
    def display_category(self, instance: Client):
        return str(instance.category)


    @display(description="Описание", label=True)
    def display_description(self, instance: Client):
        return instance.description

    @action(
        description=_("Rebuild Index"),
        url_path="actions-row-custom-url",
        permissions=[
            "custom_actions_row",
            "another_custom_actions_row",
        ],
    )
    def custom_actions_row(self, request, object_id):
        messages.success(
            request, f"Row action has been successfully executed. Object ID {object_id}"
        )
        return redirect(
            request.headers.get("referer")
            or reverse_lazy("admin:formula_constructor_changelist")
        )

    def has_custom_actions_row_permission(self, request, object_id=None):
        return request.user.is_superuser

    def has_another_custom_actions_row_permission(self, request, object_id=None):
        return request.user.is_staff

    @action(description=_("Reindex Cache"), url_path="actions-row-reindex-cache")
    def custom_actions_row2(self, request, object_id):
        messages.success(
            request, f"Row action has been successfully executed. Object ID {object_id}"
        )
        return redirect(
            request.headers.get("referer")
            or reverse_lazy("admin:formula_constructor_changelist")
        )



@admin.register(Client)
class ClientAdmin(GuardedModelAdmin, SimpleHistoryAdmin, ClientAdminMixin):
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "first_name",
                    "last_name",
                    "middle_name",
                    "category",
                    "phone",
                    "description",
                    "born_at",
                ]
            },
        ),
    #     (
    #         _("Boolean fields"),
    #         {
    #             "classes": ["tab"],
    #             "fields": [
    #                 "is_active",
    #             ],
    #         },
    #     ),
    ]

    actions_list = ["changelist_action1"]
    actions_detail = ["change_detail_action",]

#     date_hierarchy = "date"
#     search_fields = [
#         "circuit__name",
#         "circuit__city",
#         "circuit__country",
#         "winner__first_name",
#         "winner__last_name",
#     ]
#     list_filter = [
#         ("circuit", RelatedCheckboxFilter),
#         ("year", RangeNumericFilter),
#         ("laps", SingleNumericFilter),
#         ("date", RangeDateFilter),
#         ("created_at", RangeDateTimeFilter),
#     ]
#     list_filter_sheet = False
#     list_filter_submit = True
#     raw_id_fields = ["circuit", "winner"]
#     list_display = ["circuit", "winner", "year", "laps", "date"]
#     list_fullwidth = True
#     autocomplete_fields = ["circuit", "winner"]


    def get_urls(self):
        return super().get_urls() + [
            path(
                "crispy-form",
                self.admin_site.admin_view(CrispyFormView.as_view(model_admin=self)),
                name="crispy_form",
            ),
        ]

    @action(description=_("Initialize nodes"), icon="hub")
    def changelist_action1(self, request):
        messages.success(
            request, _("Changelist action has been successfully executed.")
        )
        return redirect(reverse_lazy("admin:formula_client_changelist"))

    @action(
        description=_("Action with form"),
        url_path="change-detail-action",
        permissions=["change_detail_action"],
    )
    def change_detail_action(self, request, object_id):
        try:
            object_id = int(object_id)
        except (TypeError, ValueError) as e:
            raise Http404 from e

        object = get_object_or_404(Client, pk=object_id)

        class SomeForm(forms.Form):
            # It is important to set a widget coming from Unfold
            from_date = forms.SplitDateTimeField(
                label="From Date", widget=UnfoldAdminSplitDateTimeWidget, required=False
            )
            to_date = forms.SplitDateTimeField(
                label="To Date", widget=UnfoldAdminSplitDateTimeWidget, required=False
            )
            note = forms.CharField(label=_("Note"), widget=UnfoldAdminTextInputWidget)

            class Media:
                js = [
                    "admin/js/vendor/jquery/jquery.js",
                    "admin/js/jquery.init.js",
                    "admin/js/calendar.js",
                    "admin/js/admin/DateTimeShortcuts.js",
                    "admin/js/core.js",
                ]

        form = SomeForm(request.POST or None)

        if request.method == "POST" and form.is_valid():
            # form.cleaned_data["note"]

            messages.success(request, _("Change detail action has been successful."))

            return redirect(
                reverse_lazy("admin:formula_client_change", args=[object_id])
            )

        return render(
            request,
            "formula/client_action.html",
            {
                "form": form,
                "object": object,
                "title": _("Change detail action for {}").format(object),
                **self.admin_site.each_context(request),
            },
        )

    def has_change_detail_action_permission(self, request, object_id=None):
        return request.user.is_superuser

    @action(description=_("Revalidate cache"), permissions=["revalidate_cache"])
    def change_detail_action1(self, request, object_id):
        messages.success(
            request, _("Change detail action has been successfully executed.")
        )
        return redirect(reverse_lazy("admin:formula_client_change", args=[object_id]))

    def has_revalidate_cache_permission(self, request, object_id):
        return request.user.is_superuser

    @action(description=_("Deactivate object"))
    def change_detail_action2(self, request, object_id):
        messages.success(
            request, _("Change detail action has been successfully executed.")
        )
        return redirect(reverse_lazy("admin:formula_client_change", args=[object_id]))


class ClientCustomCheckboxFilter(CheckboxFilter):
    title = _("Custom status")
    parameter_name = "custom_status"

    def lookups(self, request, model_admin):
        return ActivityCategory.choices

    def queryset(self, request, queryset):
        if self.value() not in EMPTY_VALUES:
            return queryset.filter(status__in=self.value())
        elif self.parameter_name in self.used_parameters:
            return queryset.filter(status=self.used_parameters[self.parameter_name])

        return queryset


class SalarySliderNumericFilter(SliderNumericFilter):
    MAX_DECIMALS = 2


@admin.register(BookingWithFilters)
class BookingWithFiltersAdmin(ClientAdminMixin):
    list_fullwidth = True
    list_filter = [
        FullNameFilter,
        # ("constructors", AutocompleteSelectMultipleFilter),
        ("room__name", RelatedDropdownFilter),
        # ("salary", SalarySliderNumericFilter),
        ("room__category", ChoicesCheckboxFilter),
        # ("category", AllValuesCheckboxFilter),
        # DriverCustomCheckboxFilter,
        ("is_active", BooleanRadioFilter),
    ]
    list_filter_sheet = False
    list_filter_submit = True


@register_component
class ClientActiveComponent(BaseComponent):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["children"] = render_to_string(
            "formula/helpers/kpi_progress.html",
            {
                "total": Client.objects.filter(category=ActivityCategory.STANDARD).count(),
                "progress": "positive",
                "percentage": "2.8%",
            },
        )
        return context


@register_component
class ClientInactiveComponent(BaseComponent):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["children"] = render_to_string(
            "formula/helpers/kpi_progress.html",
            {
                "total": Client.objects.filter(category=ActivityCategory.BEDRIDDEN).count(),
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
