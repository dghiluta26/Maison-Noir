from rest_framework.permissions import BasePermission


class IsAdminRole(BasePermission):
    """
    Allows access only to users with role "admin".

    Visitors get 401 (not logged in); logged-in customers get 403.
    Use on every admin-only endpoint: permission_classes = [IsAdminRole].
    """

    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and getattr(user, "is_admin", False))
