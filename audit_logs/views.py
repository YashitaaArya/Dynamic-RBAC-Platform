from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from permissions_app.mixins import PermissionRequiredMixin
from .models import AuditLog


class AuditLogListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = AuditLog
    template_name = "audit_logs/audit_log_list.html"
    context_object_name = "audit_logs"
    feature_code = "AUDIT_LOGS"
    permission_action = "view"

    def get_queryset(self):
        user = self.request.user
        queryset = AuditLog.objects.select_related("user", "organization")
        if user.is_superuser:
            return queryset
        if hasattr(user, "profile") and user.profile.organization:
            return queryset.filter(organization=user.profile.organization)
        return queryset.none()
