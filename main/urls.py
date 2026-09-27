from django.urls import path
from main.views import (
    show_main, 
    show_experience, 
    create_experience,
    update_experience,
    delete_experience,
    get_experience_json,
    show_interest, 
    create_interest, 
    delete_interest, 
    get_interest_json,
    register,
    logout_user,
    login_user,
    toggle_star_interest,
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),

    path("experience/", show_experience, name="show_experience"),
    path("experience/add/", create_experience, name="create_experience"),
    path("experience/<uuid:experience_id>/edit/", update_experience, name="update_experience"),
    path("experience/<uuid:experience_id>/delete/", delete_experience, name="delete_experience"),
    path("api/experience/", get_experience_json, name="get_experience_json"),


    path("interest/", show_interest, name="show_interest"),
    path("interest/add/", create_interest, name="create_interest"),
    path("interest/<int:interest_id>/delete/",delete_interest,name="delete_interest"),
    path("api/interest/", get_interest_json, name="get_interest_json"),
    path("interest/<int:interest_id>/star/", toggle_star_interest, name="toggle_star_interest"),

    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
]