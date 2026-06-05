from django.urls import path
from .views import (
    OrganizationListView,
    OrganizationCreateView,
    OrganizationUpdateView,
    OrganizationDeleteView,
)

urlpatterns = [
    path("", OrganizationListView.as_view(), name="organization_list"),
    path("create/", OrganizationCreateView.as_view(), name="organization_create"),
    path("<uuid:pk>/edit/", OrganizationUpdateView.as_view(), name="organization_update"),
    path("<uuid:pk>/delete/", OrganizationDeleteView.as_view(), name="organization_delete"),
]
