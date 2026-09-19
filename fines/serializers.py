from decimal import Decimal

from rest_framework import serializers

from loans.models import Loan

from .models import Fine, Payment


class FineSerializer(serializers.ModelSerializer):

    loan = serializers.PrimaryKeyRelatedField(
        queryset=Loan.objects.all(),
    )

    class Meta:
        model = Fine

        fields = [
            "id",
            "loan",
            "amount",
            "reason",
            "status",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "status",
            "created_at",
        ]

    def validate_loan(self, loan):

        if hasattr(loan, "fine"):
            raise serializers.ValidationError(
                "This loan already has a fine."
            )

        return loan

    def create(self, validated_data):

        return Fine.objects.create(
            status=Fine.Status.UNPAID,
            **validated_data
        )


class PaymentSerializer(serializers.ModelSerializer):

    fine = serializers.PrimaryKeyRelatedField(
        queryset=Fine.objects.all(),
    )

    class Meta:
        model = Payment

        fields = [
            "id",
            "fine",
            "amount",
            "payment_method",
            "reference",
            "paid_at",
        ]

        read_only_fields = [
            "id",
            "paid_at",
        ]

    def validate(self, attrs):

        fine = attrs["fine"]
        amount = attrs["amount"]

        if amount <= Decimal("0.00"):
            raise serializers.ValidationError(
                {
                    "amount": (
                        "Payment amount must be greater than zero."
                    )
                }
            )

        total_paid = sum(
            payment.amount
            for payment in fine.payments.all()
        )

        remaining = fine.amount - total_paid

        if amount > remaining:
            raise serializers.ValidationError(
                {
                    "amount": (
                        f"Payment exceeds the remaining fine "
                        f"balance of {remaining}."
                    )
                }
            )

        if fine.status in [
            Fine.Status.PAID,
            Fine.Status.WAIVED,
        ]:
            raise serializers.ValidationError(
                {
                    "fine": (
                        "This fine cannot receive "
                        "any more payments."
                    )
                }
            )

        return attrs