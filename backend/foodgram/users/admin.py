from django.contrib import admin

from .models import Follow, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'last_login',
        'is_staff',
        'is_active',
        'date_joined',
        'password',
    )
    list_filter = (
        'username',
        'email',
        'is_staff'
    )


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'author'
    )
