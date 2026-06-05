from rest_framework import permissions

from .utils import has_permission, resolve_action


class FeaturePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        feature_code = getattr(view, "feature_code", None)
        if not feature_code:
            return True
        action = getattr(view, "permission_action", None) or getattr(view, "action", None)
        if not action:
            action = "view"
        action = resolve_action(action)
        return has_permission(request.user, feature_code, action)
