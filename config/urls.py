from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path(
        "admin/",
        admin.site.urls,
    ),

    path(
        "api/",
        include("users.urls"),
    ),

    path(
        "api/",
        include("catalog.urls"),
    ),

    path(
        "api/",
        include("loans.urls"),
    ),

    path(
        "api/",
        include("reservations.urls"),
    ),

    path(
        "api/",
        include("fines.urls"),
    ),
]