from django.db import transaction

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Fine, Payment
from .serializers import (
    FineSerializer,
    PaymentSerializer,
)


class FineListCreateView(APIView):

    def get(self, request):

        fines = (
            Fine.objects
            .select_related(
                "loan",
                "loan__member",
                "loan__book_copy",
                "loan__book_copy__book",
            )
            .all()
        )

        serializer = FineSerializer(
            fines,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):

        serializer = FineSerializer(
            data=request.data
        )

        if serializer.is_valid():

            fine = serializer.save()

            return Response(
                FineSerializer(fine).data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class PaymentListCreateView(APIView):

    def get(self, request):

        payments = (
            Payment.objects
            .select_related("fine")
            .all()
        )

        serializer = PaymentSerializer(
            payments,
            many=True
        )

        return Response(serializer.data)

    @transaction.atomic
    def post(self, request):

        serializer = PaymentSerializer(
            data=request.data
        )

        if serializer.is_valid():

            payment = serializer.save()

            fine = payment.fine

            total_paid = sum(
                payment.amount
                for payment in fine.payments.all()
            )

            if total_paid >= fine.amount:
                fine.status = Fine.Status.PAID

            else:
                fine.status = Fine.Status.PARTIALLY_PAID

            fine.save(
                update_fields=["status"]
            )

            return Response(
                PaymentSerializer(payment).data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )