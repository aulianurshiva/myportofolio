from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsPortfolioOwnerOrEditorOrReadOnly(BasePermission):
    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        return (
            request.method in ("PUT", "PATCH")
            and request.user.groups.filter(name="Editor").exists()
        )