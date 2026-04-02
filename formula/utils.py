import random

from django.conf import settings
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


def badge_callback(request):
    return f"{random.randint(1, 9)}"


def booking_link_callback(request):
    if (
        reverse_lazy("admin:formula_booking_changelist") in request.path
        or request.path == reverse_lazy("admin:formula_booking_changelist")
        or request.path == reverse_lazy("admin:crispy_formset")
    ):
        return True

    return False


def booking_list_link_callback(request):
    if request.path == reverse_lazy("admin:formula_booking_changelist"):
        return True

    if str(reverse_lazy("admin:formula_booking_changelist")) in request.path:
        return True

    return False


def booking_list_sublink_callback(request):
    if str(reverse_lazy("admin:crispy_formset")) in request.path:
        return False

    if request.path == reverse_lazy("admin:formula_booking_changelist"):
        return True

    if str(reverse_lazy("admin:formula_booking_changelist")) in request.path:
        return True

    return False


def search_models_callback(request):
    return [
        "formula.booking",
    ]


def show_history_callback(request):
    return True
