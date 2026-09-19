from django.urls import path

from .views import (
    ReservationCancelView,
    ReservationFulfillView,
    ReservationListCreateView,
    ReservationReadyView,
)


urlpatterns = [
    path(
        "reservations/",
        ReservationListCreateView.as_view(),
        name="reservation-list-create",
    ),

    path(
        "reservations/<int:pk>/ready/",
        ReservationReadyView.as_view(),
        name="reservation-ready",
    ),

    path(
        "reservations/<int:pk>/cancel/",
        ReservationCancelView.as_view(),
        name="reservation-cancel",
    ),

    path(
        "reservations/<int:pk>/fulfill/",
        ReservationFulfillView.as_view(),
        name="reservation-fulfill",
    ),
]