from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from landing.views import HomeView, BookView, CrispyFormView, ResultView

urlpatterns = (
    [
        path("", HomeView.as_view(), name="home"),
        path("book/", BookView.as_view(), name="book"),
        path("result/", ResultView.as_view(), name="result"),
        path("crispy/", CrispyFormView.as_view(), name="crispy"),
    ]
)
