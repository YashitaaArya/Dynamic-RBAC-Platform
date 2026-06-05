from django.urls import path
from .views import (
    FeatureListView,
    RoleCreateView,
    RoleDeleteView,
    RoleListView,
    RolePermissionUpdateView,
    RoleUpdateView,
)

urlpatterns = [
    path("", RoleListView.as_view(), name="role_list"),
    path("create/", RoleCreateView.as_view(), name="role_create"),
    path("<uuid:pk>/edit/", RoleUpdateView.as_view(), name="role_update"),
    path("<uuid:pk>/delete/", RoleDeleteView.as_view(), name="role_delete"),
    path("<uuid:pk>/permissions/", RolePermissionUpdateView.as_view(), name="role_permissions"),
    path("features/", FeatureListView.as_view(), name="feature_list"),
]
