from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)


class IsOwnerOrModerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        if request.method not in permissions.SAFE_METHODS:
            return (request.user.is_authenticated
                    and (obj.author == request.user
                         or request.user.is_superuser
                         or request.user.role == 'admin'
                         or request.user.role == 'moderator'))
        return True


class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (
                    request.user.is_superuser
                    or request.user.role == 'admin'
                ))


class AdminUnsafeOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method not in permissions.SAFE_METHODS:
            return (request.user.is_authenticated
                    and (
                        request.user.is_superuser
                        or request.user.role == 'admin'
                    ))
        return True


class AdminOnlyExceptUpdateDestroy(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method not in ['PATCH', 'DELETE']:
            return (request.user.is_authenticated
                    and (request.user.is_superuser
                         or request.user.role == 'admin'))
        return True

    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated
                and (request.user.is_superuser
                     or request.user.role == 'admin'))
