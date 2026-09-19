from django.contrib import admin

from .models import Member


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = (
        "member_number",
        "user",
        "phone",
        "status",
        "membership_date",
    )

    list_filter = (
        "status",
        "membership_date",
    )

    search_fields = (
        "member_number",
        "user__username",
        "user__email",
        "phone",
    )