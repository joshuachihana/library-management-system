from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Member


class MemberSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source="user.username"
    )

    email = serializers.EmailField(
        source="user.email"
    )

    password = serializers.CharField(
        write_only=True,
        source="user.password"
    )

    class Meta:
        model = Member
        fields = [
            "id",
            "username",
            "email",
            "password",
            "member_number",
            "phone",
            "address",
            "membership_date",
            "status",
        ]

        read_only_fields = [
            "id",
            "membership_date",
        ]

    def create(self, validated_data):

        user_data = validated_data.pop("user")

        user = User.objects.create_user(
            username=user_data["username"],
            email=user_data["email"],
            password=user_data["password"],
        )

        member = Member.objects.create(
            user=user,
            **validated_data
        )

        return member