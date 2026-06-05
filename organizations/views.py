from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from audit_logs.services import record_audit_log
from permissions_app.mixins import PermissionRequiredMixin
from .forms import OrganizationForm
from .models import Organization


class OrganizationListView(LoginRequiredMixin, ListView):
    model = Organization
    template_name = "organizations/organization_list.html"
    context_object_name = "organizations"

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Organization.objects.all()
        if hasattr(user, "profile") and user.profile.organization:
            return Organization.objects.filter(id=user.profile.organization_id)
        return Organization.objects.none()


class OrganizationCreateView(PermissionRequiredMixin, CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = "organizations/organization_form.html"
    success_url = reverse_lazy("organization_list")
    feature_code = "ORG_MANAGEMENT"
    permission_action = "create"

    def form_valid(self, form):
        organization = form.save()
        self.object = organization
        record_audit_log(self.request.user, "create", organization, before_data={}, after_data={"name": organization.name})
        return redirect(self.success_url)


class OrganizationUpdateView(PermissionRequiredMixin, UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = "organizations/organization_form.html"
    success_url = reverse_lazy("organization_list")
    feature_code = "ORG_MANAGEMENT"
    permission_action = "update"

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_superuser:
            return qs
        if hasattr(user, "profile") and user.profile.organization:
            return qs.filter(id=user.profile.organization_id)
        return qs.none()

    def form_valid(self, form):
        previous_name = self.object.name if self.object else None
        previous_description = self.object.description if self.object else None
        organization = form.save()
        self.object = organization
        record_audit_log(
            self.request.user,
            "update",
            organization,
            before_data={"name": previous_name, "description": previous_description},
            after_data={"name": organization.name, "description": organization.description},
        )
        return redirect(self.success_url)


class OrganizationDeleteView(PermissionRequiredMixin, DeleteView):
    model = Organization
    template_name = "organizations/organization_confirm_delete.html"
    success_url = reverse_lazy("organization_list")
    feature_code = "ORG_MANAGEMENT"
    permission_action = "delete"

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_superuser:
            return qs
        if hasattr(user, "profile") and user.profile.organization:
            return qs.filter(id=user.profile.organization_id)
        return qs.none()

    def delete(self, request, *args, **kwargs):
        organization = self.get_object()
        record_audit_log(request.user, "delete", organization, before_data={"name": organization.name, "description": organization.description}, after_data={})
        return super().delete(request, *args, **kwargs)
