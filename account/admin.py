from django.contrib import admin
from .models import CustomUser, OTP, UserState, UserChallenge
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'is_verified', 'is_staff')
    search_fields = ('email', 'username')
    ordering = ('email',)
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_verified',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(OTP)
admin.site.register(UserState)
admin.site.register(UserChallenge)