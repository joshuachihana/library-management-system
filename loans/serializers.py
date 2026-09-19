from datetime import date

from django.utils import timezone
from rest_framework import serializers

from catalog.models import BookCopy
from users.models import Member

from .models import Loan


class LoanSerializer(serializers.ModelSerializer):

    member = serializers.PrimaryKeyRelatedField(
        queryset=Member.objects.all(),
    )

    book_copy = serializers.PrimaryKeyRelatedField(
        queryset=BookCopy.objects.all(),
    )

    class Meta:
        model = Loan

        fields = [
            "id",
            "member",
            "book_copy",
            "borrowed_at",
            "due_date",
            "returned_at",
            "status",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "borrowed_at",
            "returned_at",
            "status",
            "created_at",
        ]

    def validate(self, attrs):

        member = attrs["member"]
        book_copy = attrs["book_copy"]

        if member.status != Member.Status.ACTIVE:
            raise serializers.ValidationError(
                {
                    "member": (
                        "This member is not active "
                        "and cannot borrow books."
                    )
                }
            )

        if book_copy.status != BookCopy.Status.AVAILABLE:
            raise serializers.ValidationError(
                {
                    "book_copy": (
                        "This book copy is not available "
                        "for borrowing."
                    )
                }
            )

        return attrs

    def create(self, validated_data):

        return Loan.objects.create(
            status=Loan.Status.ACTIVE,
            **validated_data
        )


class LoanReturnSerializer(serializers.ModelSerializer):

    class Meta:
        model = Loan

        fields = [
            "returned_at",
            "status",
        ]

        read_only_fields = [
            "returned_at",
            "status",
        ]

    def validate(self, attrs):

        if self.instance.status == Loan.Status.RETURNED:
            raise serializers.ValidationError(
                "This loan has already been returned."
            )

        if self.instance.status == Loan.Status.LOST:
            raise serializers.ValidationError(
                "A lost loan cannot be returned normally."
            )

        return attrs

    def update(self, instance, validated_data):

        instance.returned_at = timezone.now()
        instance.status = Loan.Status.RETURNED

        instance.save(
            update_fields=[
                "returned_at",
                "status",
            ]
        )

        return instance


class LoanOverdueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Loan

        fields = [
            "status",
        ]

        read_only_fields = [
            "status",
        ]

    def validate(self, attrs):

        if self.instance.status != Loan.Status.ACTIVE:
            raise serializers.ValidationError(
                "Only active loans can be marked as overdue."
            )

        if self.instance.due_date >= date.today():
            raise serializers.ValidationError(
                "This loan is not overdue yet."
            )

        return attrs

    def update(self, instance, validated_data):

        instance.status = Loan.Status.OVERDUE

        instance.save(
            update_fields=["status"]
        )

        return instance