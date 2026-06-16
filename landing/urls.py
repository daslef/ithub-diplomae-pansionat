from django.urls import path

from landing.views import BookView, HomeView, ResultView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("book/", BookView.as_view(), name="book"),
    path("result/", ResultView.as_view(), name="result"),
]
