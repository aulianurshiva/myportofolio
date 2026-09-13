from django.urls import path

from main.views import show_main, show_experience, show_interest

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("interest/", show_interest, name="show_interest"),
]