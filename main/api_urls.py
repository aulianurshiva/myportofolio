from django.urls import path

from main import api_views


app_name = "api"

urlpatterns = [
    path(
        "interests/",
        api_views.interest_list,
        name="interest-list",
    ),
    path(
        "interests/<int:interest_id>/",
        api_views.interest_detail,
        name="interest-detail",
    ),
    path(
        "interests/<int:interest_id>/star/",
        api_views.interest_star,
        name="interest-star",
    ),
]