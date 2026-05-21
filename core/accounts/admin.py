from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, OtpCode, Profile, AddressUser

# Register your models here.

class AddressUserAdminInline(admin.StackedInline):
    model = AddressUser
    extra = 1
    verbose_name_plural = 'addresses'

class ProfileUserAdminInline(admin.StackedInline):
    model = Profile


class CustomUserAdmin(UserAdmin):
    list_display = ("phone","email", "is_superuser", "is_active", "is_verified")
    list_filter = ("phone", "email", "is_superuser", "is_active", "is_verified")
    search_fields = ("email","phone")
    ordering = ("email","phone")

    readonly_fields = (
        "created_date",
        "updated_date",
    )

    inlines = [ProfileUserAdminInline, AddressUserAdminInline]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "phone",
                    "email",
                    "password",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_verified",
                )
            },
        ),
        (
            "Group Permissions",
            {"fields": ("groups", "user_permissions")},
        ),
        (
            "Important Dates",
            {"fields": ("created_date", "updated_date", "last_login")},
        ),
    )

    add_fieldsets = (
        (None, {"fields": ("phone","email", "password1", "password2")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_verified",
                )
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)


@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ['user__email', 'expired_at', 'is_expired']

admin.site.register(Profile)
