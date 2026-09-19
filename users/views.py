from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Member
from .serializers import MemberSerializer


class MemberListCreateView(APIView):

    def get(self, request):

        members = Member.objects.select_related("user").all()

        serializer = MemberSerializer(
            members,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):

        serializer = MemberSerializer(
            data=request.data
        )

        if serializer.is_valid():

            member = serializer.save()

            return Response(
                MemberSerializer(member).data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )