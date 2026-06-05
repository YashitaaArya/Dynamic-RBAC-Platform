from rest_framework import viewsets

from audit_logs.services import record_audit_log
from .models import Organization
from .serializers import OrganizationSerializer


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return self.queryset
        if hasattr(user, "profile") and user.profile.organization:
            return self.queryset.filter(id=user.profile.organization_id)
        return self.queryset.none()

    def perform_create(self, serializer):
        organization = serializer.save()
        record_audit_log(self.request.user, "create", organization, before_data={}, after_data={"name": organization.name})

    def perform_update(self, serializer):
        organization = serializer.instance
        before_data = {"name": organization.name, "description": organization.description}
        serializer.save()
        record_audit_log(self.request.user, "update", organization, before_data=before_data, after_data={"name": organization.name})

    def perform_destroy(self, instance):
        record_audit_log(self.request.user, "delete", instance, before_data={"name": instance.name}, after_data={})
        instance.delete()
