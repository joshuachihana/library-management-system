from django.urls import path

from .views import (
    FineListCreateView,
    PaymentListCreateView,
)


urlpatterns = [
    path(
        "fines/",
        FineListCreateView.as_view(),
        name="fine-list-create",
    ),

    path(
        "payments/",
        PaymentListCreateView.as_view(),
        name="payment-list-create",
    ),
]