from django.db import models


class Fine(models.Model):

    class Status(models.TextChoices):
        UNPAID = "UNPAID", "Unpaid"
        PARTIALLY_PAID = "PARTIALLY_PAID", "Partially Paid"
        PAID = "PAID", "Paid"
        WAIVED = "WAIVED", "Waived"

    loan = models.OneToOneField(
        "loans.Loan",
        on_delete=models.PROTECT,
        related_name="fine",
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    reason = models.CharField(
        max_length=255,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.UNPAID,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.loan} - {self.amount}"


class Payment(models.Model):

    class PaymentMethod(models.TextChoices):
        CASH = "CASH", "Cash"
        BANK = "BANK", "Bank"
        MOBILE_MONEY = "MOBILE_MONEY", "Mobile Money"
        CARD = "CARD", "Card"

    fine = models.ForeignKey(
        Fine,
        on_delete=models.PROTECT,
        related_name="payments",
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
    )

    reference = models.CharField(
        max_length=100,
        blank=True,
    )

    paid_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.fine} - {self.amount}"