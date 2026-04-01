import random

from django.conf import settings
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


def environment_callback(request):
    if settings.DEBUG:
        return [_("Development"), "primary"]

    return [_("Production"), "primary"]


def badge_callback(request):
    return f"{random.randint(1, 9)}"


def permission_callback(request):
    return True


def client_link_callback(request):
    if (
        reverse_lazy("admin:formula_client_changelist") in request.path
        or request.path == reverse_lazy("admin:formula_bookingwithfilters_changelist")
        or request.path == reverse_lazy("admin:crispy_form")
        or request.path == reverse_lazy("admin:crispy_formset")
    ):
        return True

    return False


def client_list_link_callback(request):
    if request.path == reverse_lazy("admin:formula_client_changelist"):
        return True

    if str(reverse_lazy("admin:formula_client_changelist")) in request.path:
        return True

    if str(reverse_lazy("admin:formula_bookingwithfilters_changelist")) in request.path:
        return True

    return False


def client_list_sublink_callback(request):
    if str(reverse_lazy("admin:crispy_form")) in request.path:
        return False

    if str(reverse_lazy("admin:crispy_formset")) in request.path:
        return False

    if request.path == reverse_lazy("admin:formula_client_changelist"):
        return True

    if str(reverse_lazy("admin:formula_client_changelist")) in request.path:
        return True

    return False


def search_models_callback(request):
    return [
        "formula.client",
    ]


def show_history_callback(request):
    return True
