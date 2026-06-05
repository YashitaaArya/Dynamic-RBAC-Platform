from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from accounts.models import UserProfile
from audit_logs.models import AuditLog
from organizations.models import Organization
from permissions_app.mixins import PermissionRequiredMixin
from roles.models import Feature, Role


class DashboardView(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = "dashboard/dashboard.html"
    feature_code = "DASHBOARD"
    permission_action = "view"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_superuser:
            context.update({
                "total_organizations": Organization.objects.count(),
                "total_users": UserProfile.objects.count(),
                "total_roles": Role.objects.count(),
                "total_features": Feature.objects.count(),
                "recent_audit_logs": AuditLog.objects.select_related("user", "organization")[:8],
            })
        else:
            organization = getattr(user.profile, "organization", None)
            context.update({
                "total_organizations": 1 if organization else 0,
                "total_users": UserProfile.objects.filter(organization=organization).count(),
                "total_roles": Role.objects.filter(organization=organization).count(),
                "total_features": Feature.objects.count(),
                "recent_audit_logs": AuditLog.objects.filter(organization=organization).select_related("user", "organization")[:8],
            })
        return context
