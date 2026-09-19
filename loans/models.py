class Loan(models.Model):

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        RETURNED = "RETURNED", "Returned"
        OVERDUE = "OVERDUE", "Overdue"
        LOST = "LOST", "Lost"

    member = models.ForeignKey(
        "users.Member",
        on_delete=models.PROTECT,
        related_name="loans",
    )

    book_copy = models.ForeignKey(
        "catalog.BookCopy",
        on_delete=models.PROTECT,
        related_name="loans",
    )

    borrowed_at = models.DateTimeField(auto_now_add=True)

    due_date = models.DateField()

    returned_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["book_copy"],
                condition=models.Q(
                    status__in=["ACTIVE", "OVERDUE"]
                ),
                name="one_active_loan_per_book_copy",
            ),
        ]

    def __str__(self):
        return (
            f"{self.member.member_number} - "
            f"{self.book_copy.book.title}"
        )