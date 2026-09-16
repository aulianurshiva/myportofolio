from django.urls import path
from main.views import show_main, show_experience, show_interest, create_interest, delete_interest, get_interest_json

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("interest/", show_interest, name="show_interest"),
    path("interest/add/", create_interest, name="create_interest"),
    path("interest/<int:interest_id>/delete/",delete_interest,name="delete_interest"),
    path("api/interest/", get_interest_json, name="get_interest_json"),
]