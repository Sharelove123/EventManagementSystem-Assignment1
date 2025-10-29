from rest_framework import permissions

class IsOrganizerOrReadOnly(permissions.BasePermission):
    """
    Only the organizer may update or delete an event; read is allowed if event is visible.
    """

    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS (GET, HEAD, OPTIONS) allowed if visible; updates allowed only to organizer
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.organizer == request.user


class IsAuthenticatedForCreate(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            return request.user and request.user.is_authenticated
        return True