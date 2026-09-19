from rest_framework import serializers

from catalog.models import Book
from users.models import Member

from .models import Reservation


class ReservationSerializer(serializers.ModelSerializer):

    member = serializers.PrimaryKeyRelatedField(
        queryset=Member.objects.all(),
    )

    book = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(),
    )

    class Meta:
        model = Reservation

        fields = [
            "id",
            "member",
            "book",
            "reserved_at",
            "expires_at",
            "status",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "reserved_at",
            "status",
            "created_at",
        ]

    def validate(self, attrs):

        member = attrs["member"]
        book = attrs["book"]

        if member.status != Member.Status.ACTIVE:
            raise serializers.ValidationError(
                {
                    "member": (
                        "This member is not active "
                        "and cannot make reservations."
                    )
                }
            )

        existing_reservation = Reservation.objects.filter(
            member=member,
            book=book,
            status__in=[
                Reservation.Status.WAITING,
                Reservation.Status.READY,
            ],
        ).exists()

        if existing_reservation:
            raise serializers.ValidationError(
                {
                    "book": (
                        "This member already has an "
                        "active reservation for this book."
                    )
                }
            )

        return attrs

    def create(self, validated_data):

        return Reservation.objects.create(
            status=Reservation.Status.WAITING,
            **validated_data
        )


class ReservationReadySerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = [
            "expires_at",
            "status",
        ]

        read_only_fields = [
            "status",
        ]

    def validate(self, attrs):

        if self.instance.status != Reservation.Status.WAITING:
            raise serializers.ValidationError(
                "Only waiting reservations can be marked as ready."
            )

        return attrs

    def update(self, instance, validated_data):

        instance.status = Reservation.Status.READY

        instance.expires_at = validated_data.get(
            "expires_at",
            instance.expires_at,
        )

        instance.save(
            update_fields=[
                "status",
                "expires_at",
            ]
        )

        return instance


class ReservationCancelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = [
            "status",
        ]

        read_only_fields = [
            "status",
        ]

    def validate(self, attrs):

        if self.instance.status not in [
            Reservation.Status.WAITING,
            Reservation.Status.READY,
        ]:
            raise serializers.ValidationError(
                "This reservation cannot be cancelled."
            )

        return attrs

    def update(self, instance, validated_data):

        instance.status = Reservation.Status.CANCELLED

        instance.save(
            update_fields=["status"]
        )

        return instance


class ReservationFulfillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = [
            "status",
        ]

        read_only_fields = [
            "status",
        ]

    def validate(self, attrs):

        if self.instance.status != Reservation.Status.READY:
            raise serializers.ValidationError(
                "Only ready reservations can be fulfilled."
            )

        return attrs

    def update(self, instance, validated_data):

        instance.status = Reservation.Status.FULFILLED

        instance.save(
            update_fields=["status"]
        )

        return instance