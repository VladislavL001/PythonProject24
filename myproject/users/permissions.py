from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """
    Разрешение только для пользователей из группы Moderators.
    """

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Moderators").exists()


class IsOwner(BasePermission):
    """
    Разрешение только владельцу объекта.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
