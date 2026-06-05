from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from audit_logs.services import record_audit_log
from .models import Feature, Role, RoleFeaturePermission
from .serializers import FeatureSerializer, RoleFeaturePermissionSerializer, RoleSerializer


class OrganizationScopedViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return super().get_queryset()
        if hasattr(user, "profile") and user.profile.organization:
            return super().get_queryset().filter(organization=user.profile.organization)
        return self.queryset.none()


class RoleViewSet(OrganizationScopedViewSet):
    queryset = Role.objects.select_related("organization")
    serializer_class = RoleSerializer

    def perform_create(self, serializer):
        organization = None
        if self.request.user.is_superuser:
            organization = serializer.validated_data.get("organization") or getattr(getattr(self.request.user, "profile", None), "organization", None)
        else:
            organization = getattr(getattr(self.request.user, "profile", None), "organization", None)

        if not organization:
            raise PermissionDenied("Organization must be set for role creation.")

        serializer.save(created_by=self.request.user, organization=organization)
        record_audit_log(self.request.user, "create", serializer.instance, before_data={}, after_data={"name": serializer.instance.name})

    def perform_update(self, serializer):
        before_data = {"name": serializer.instance.name}
        serializer.save()
        record_audit_log(self.request.user, "update", serializer.instance, before_data=before_data, after_data={"name": serializer.instance.name})

    def perform_destroy(self, instance):
        record_audit_log(self.request.user, "delete", instance, before_data={"name": instance.name}, after_data={})
        instance.delete()


class FeatureViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer


class RoleFeaturePermissionViewSet(viewsets.ModelViewSet):
    queryset = RoleFeaturePermission.objects.select_related("role", "feature")
    serializer_class = RoleFeaturePermissionSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return self.queryset
        if hasattr(user, "profile") and user.profile.organization:
            return self.queryset.filter(role__organization=user.profile.organization)
        return self.queryset.none()

    def perform_create(self, serializer):
        serializer.save()
        record_audit_log(self.request.user, "create_permission", serializer.instance, before_data={}, after_data={"role": serializer.instance.role.name, "feature": serializer.instance.feature.code})

    def perform_update(self, serializer):
        before_data = {"permissions": serializer.instance.can_view}
        serializer.save()
        record_audit_log(self.request.user, "update_permission", serializer.instance, before_data=before_data, after_data={"role": serializer.instance.role.name, "feature": serializer.instance.feature.code})

    def perform_destroy(self, instance):
        record_audit_log(self.request.user, "delete_permission", instance, before_data={"role": instance.role.name, "feature": instance.feature.code}, after_data={})
        instance.delete()
