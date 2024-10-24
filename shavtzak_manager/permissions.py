from rest_framework import permissions

from shavtzak_manager.models import UserTypeChoices


class IsEntityInitializer(permissions.BasePermission):
    """
    Global permission check for blocked IPs.
    """

    def has_permission(self, request, view):
        return request.user.user_system_custom_fields.user_type == UserTypeChoices.ENTITY_INITIALIZER.value
