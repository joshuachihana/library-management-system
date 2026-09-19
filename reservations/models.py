from django.db import models


class Reservation(models.Model):

    class Status(models.TextChoices):
        WAITING = "WAITING", "Waiting"
        READY = "READY", "Ready"
        FULFILLED = "FULFILLED", "Fulfilled"
        CANCELLED = "CANCELLED", "Cancelled"
        EXPIRED = "EXPIRED", "Expired"

    member = models.ForeignKey(
        "users.Member",
        on_delete=models.PROTECT,
        related_name="reservations",
    )

    book = models.ForeignKey(
        "catalog.Book",
        on_delete=models.PROTECT,
        related_name="reservations",
    )

    reserved_at = models.DateTimeField(
        auto_now_add=True,
    )

    expires_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.WAITING,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["member", "book"],
                condition=models.Q(
                    status__in=["WAITING", "READY"]
                ),
                name="one_active_reservation_per_member_book",
            ),
        ]

    def __str__(self):
        return (
            f"{self.member.member_number} - "
            f"{self.book.title}"
        )