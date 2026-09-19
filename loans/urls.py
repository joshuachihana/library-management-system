from django.urls import path

from .views import (
    LoanListCreateView,
    LoanOverdueView,
    LoanReturnView,
)


urlpatterns = [
    path(
        "loans/",
        LoanListCreateView.as_view(),
        name="loan-list-create",
    ),

    path(
        "loans/<int:pk>/return/",
        LoanReturnView.as_view(),
        name="loan-return",
    ),

    path(
        "loans/<int:pk>/overdue/",
        LoanOverdueView.as_view(),
        name="loan-overdue",
    ),
]