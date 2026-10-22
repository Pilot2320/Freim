from django.urls import path

from . import views

app_name = "bugtracker"

urlpatterns = [
    path("", views.error_list, name="error_list"),
    path("", views.error_list, name="list"),
    path("<int:error_id>/", views.error_detail, name="error_detail"),
    path("<int:error_id>/", views.error_detail, name="detail"),
    path("search/", views.error_search, name="search"),
    path("statistics/", views.statistics, name="statistics"),
]
