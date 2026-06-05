from rest_framework import viewsets

from .models import AuditLog
from .serializers import AuditLogSerializer


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.select_related("user", "organization")
    serializer_class = AuditLogSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return self.queryset
        if hasattr(user, "profile") and user.profile.organization:
            return self.queryset.filter(organization=user.profile.organization)
        return self.queryset.none()
