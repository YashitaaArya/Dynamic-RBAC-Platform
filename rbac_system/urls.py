from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("dashboard.urls")),
    path("accounts/", include("accounts.urls")),
    path("organizations/", include("organizations.urls")),
    path("roles/", include("roles.urls")),
    path("audit-logs/", include("audit_logs.urls")),
    path("api/", include("api.urls")),
]
