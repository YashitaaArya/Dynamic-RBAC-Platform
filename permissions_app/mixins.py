from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse_lazy

from .utils import has_permission


class PermissionRequiredMixin:
    feature_code = None
    permission_action = "view"

    def dispatch(self, request, *args, **kwargs):
        if not self.feature_code:
            return super().dispatch(request, *args, **kwargs)
        if not has_permission(request.user, self.feature_code, self.permission_action):
            if not request.user.is_authenticated:
                return redirect(reverse_lazy("login"))
            return HttpResponseForbidden("You do not have permission to access this page.")
        return super().dispatch(request, *args, **kwargs)
