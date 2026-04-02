from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.db import models

from unfold.admin import (
    ModelAdmin,
    TabularInline,
)
from unfold.contrib.filters.admin import (
    BooleanRadioFilter,
    RelatedCheckboxFilter,
)
from unfold.contrib.forms.widgets import WysiwygWidget
from unfold.decorators import display
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

from employee.models import (
    Profile,
    User,
)

admin.site.unregister(Group)


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

    @display(description="Юзернейм")
    def display_header(self, instance: User):
        return instance.username

    @display(description="Сотрудник", boolean=True)
    def display_staff(self, instance: User):
        return instance.is_staff

    @display(description="Администратор", boolean=True)
    def display_superuser(self, instance: User):
        return instance.is_superuser

    @display(description="Дата добавления")
    def display_created(self, instance: User):
        return instance.created_at


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        return super().changelist_view(request, extra_context=extra_context)
