from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Reservation
from .serializers import (
    ReservationCancelSerializer,
    ReservationFulfillSerializer,
    ReservationReadySerializer,
    ReservationSerializer,
)


class ReservationListCreateView(APIView):

    def get(self, request):

        reservations = (
            Reservation.objects
            .select_related(
                "member",
                "member__user",
                "book",
            )
            .all()
        )

        serializer = ReservationSerializer(
            reservations,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):

        serializer = ReservationSerializer(
            data=request.data
        )

        if serializer.is_valid():

            reservation = serializer.save()

            return Response(
                ReservationSerializer(reservation).data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class ReservationReadyView(APIView):

    def patch(self, request, pk):

        try:
            reservation = Reservation.objects.get(pk=pk)

        except Reservation.DoesNotExist:

            return Response(
                {"detail": "Reservation not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = ReservationReadySerializer(
            reservation,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():

            reservation = serializer.save()

            return Response(
                ReservationSerializer(reservation).data,
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class ReservationCancelView(APIView):

    def patch(self, request, pk):

        try:
            reservation = Reservation.objects.get(pk=pk)

        except Reservation.DoesNotExist:

            return Response(
                {"detail": "Reservation not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = ReservationCancelSerializer(
            reservation,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():

            reservation = serializer.save()

            return Response(
                ReservationSerializer(reservation).data,
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class ReservationFulfillView(APIView):

    def patch(self, request, pk):

        try:
            reservation = Reservation.objects.get(pk=pk)

        except Reservation.DoesNotExist:

            return Response(
                {"detail": "Reservation not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = ReservationFulfillSerializer(
            reservation,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():

            reservation = serializer.save()

            return Response(
                ReservationSerializer(reservation).data,
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )