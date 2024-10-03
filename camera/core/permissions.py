from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission, SAFE_METHODS
from camera.accounts.models import AccountUserRole


class UserRolePermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)

        return self._is_superuser(request) or self._is_user_admin(request) or self._is_dev(request)

    @staticmethod
    def _is_superuser(request):
        try:
            return bool(
                request.user and
                request.user.is_superuser or request.user.role == AccountUserRole.Role.SUPER_USER.value
            )
        except Exception as e:
            raise PermissionDenied(f"{e}")

    @staticmethod
    def _is_user_admin(request):
        try:
            return bool(
                request.user and
                request.user.is_authenticated and
                request.user.role == AccountUserRole.Role.OPERATION_ADMIN.value
            )
        except Exception as e:
            raise PermissionDenied(f"{e}")

    @staticmethod
    def _is_dev(request):
        try:
            return bool(
                request.user and
                request.user.is_authenticated and
                request.user.role == AccountUserRole.Role.DEV.value
            )
        except Exception as e:
            raise PermissionDenied(f"{e}")


class IsSuperuserUser(UserRolePermission):
    """
    Allows access only to superuser users.
    """

    def has_permission(self, request, view):
        return self._is_superuser(request)


class IsSuperuserUserOrAdmin(UserRolePermission):

    def has_permission(self, request, view):
        return self._is_superuser(request) or self._is_user_admin(request)


class IsSuperuserUserOrDev(UserRolePermission):

    def has_permission(self, request, view):
        return self._is_superuser(request) or self._is_dev(request)


class IsSuperuserUserOrAdminOrDev(UserRolePermission):

    def has_permission(self, request, view):
        return self._is_superuser(request) or self._is_user_admin(request) or self._is_dev(request)
