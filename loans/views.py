from django.db import transaction

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    LoanOverdueSerializer,
    LoanReturnSerializer,
    LoanSerializer,
)


class LoanListCreateView(APIView):

    def get(self, request):

        loans = (
            Loan.objects
            .select_related(
                "member",
                "member__user",
                "book_copy",
                "book_copy__book",
            )
            .all()
        )

        serializer = LoanSerializer(
            loans,
            many=True
        )

        return Response(serializer.data)

    @transaction.atomic
    def post(self, request):

        serializer = LoanSerializer(
            data=request.data
        )

        if serializer.is_valid():

            loan = serializer.save()

            book_copy = loan.book_copy

            book_copy.status = book_copy.Status.BORROWED

            book_copy.save(
                update_fields=["status"]
            )

            return Response(
                LoanSerializer(loan).data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class LoanReturnView(APIView):

    @transaction.atomic
    def patch(self, request, pk):

        try:
            loan = (
                Loan.objects
                .select_related("book_copy")
                .get(pk=pk)
            )

        except Loan.DoesNotExist:

            return Response(
                {"detail": "Loan not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = LoanReturnSerializer(
            loan,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():

            loan = serializer.save()

            book_copy = loan.book_copy

            book_copy.status = book_copy.Status.AVAILABLE

            book_copy.save(
                update_fields=["status"]
            )

            return Response(
                LoanSerializer(loan).data,
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

class LoanOverdueView(APIView):

    def patch(self, request, pk):

        try:
            loan = Loan.objects.get(pk=pk)

        except Loan.DoesNotExist:

            return Response(
                {"detail": "Loan not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = LoanOverdueSerializer(
            loan,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():

            loan = serializer.save()

            return Response(
                LoanSerializer(loan).data,
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )