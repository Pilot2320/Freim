from django.urls import path

from .views import error_detail, error_list

urlpatterns = [
    path("", error_list, name="error_list"),
    path("<int:error_id>/", error_detail, name="error_detail"),
]
