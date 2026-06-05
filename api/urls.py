from django.urls import include, path
from rest_framework.routers import DefaultRouter

from accounts.api import UserViewSet
from audit_logs.api import AuditLogViewSet
from organizations.api import OrganizationViewSet
from roles.api import FeatureViewSet, RoleFeaturePermissionViewSet, RoleViewSet

router = DefaultRouter()
router.register(r"organizations", OrganizationViewSet, basename="organization")
router.register(r"roles", RoleViewSet, basename="role")
router.register(r"features", FeatureViewSet, basename="feature")
router.register(r"permissions", RoleFeaturePermissionViewSet, basename="permission")
router.register(r"users", UserViewSet, basename="user")
router.register(r"audit-logs", AuditLogViewSet, basename="auditlog")

urlpatterns = [
    path("", include(router.urls)),
]
