from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView

from audit_logs.services import record_audit_log
from permissions_app.mixins import PermissionRequiredMixin
from .forms import RoleForm
from .models import Feature, Role, RoleFeaturePermission


class RoleListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = Role
    template_name = "roles/role_list.html"
    context_object_name = "roles"
    feature_code = "ROLE_MANAGEMENT"
    permission_action = "view"

    def get_queryset(self):
        user = self.request.user
        queryset = Role.objects.select_related("organization")
        if user.is_superuser:
            return queryset
        if hasattr(user, "profile") and user.profile.organization:
            return queryset.filter(organization=user.profile.organization)
        return queryset.none()


class RoleCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Role
    form_class = RoleForm
    template_name = "roles/role_form.html"
    success_url = reverse_lazy("role_list")
    feature_code = "ROLE_MANAGEMENT"
    permission_action = "create"

    def form_valid(self, form):
        role = form.save(commit=False)
        if not hasattr(self.request.user, "profile") or not self.request.user.profile.organization:
            raise PermissionDenied("Cannot create a role without an assigned organization.")
        role.organization = self.request.user.profile.organization
        role.created_by = self.request.user
        role.save()
        self.object = role
        messages.success(self.request, "Role created successfully.")
        record_audit_log(self.request.user, "create", role, before_data={}, after_data={"name": role.name})
        return redirect(self.success_url)


class RoleUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Role
    form_class = RoleForm
    template_name = "roles/role_form.html"
    success_url = reverse_lazy("role_list")
    feature_code = "ROLE_MANAGEMENT"
    permission_action = "update"

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_superuser:
            return qs
        return qs.filter(organization=user.profile.organization)

    def form_valid(self, form):
        before_data = {"name": self.object.name, "description": self.object.description} if self.object else {}
        role = form.save()
        self.object = role
        messages.success(self.request, "Role updated successfully.")
        record_audit_log(self.request.user, "update", role, before_data=before_data, after_data={"name": role.name, "description": role.description})
        return redirect(self.success_url)


class RoleDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Role
    template_name = "roles/role_confirm_delete.html"
    success_url = reverse_lazy("role_list")
    feature_code = "ROLE_MANAGEMENT"
    permission_action = "delete"

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_superuser:
            return qs
        return qs.filter(organization=user.profile.organization)

    def delete(self, request, *args, **kwargs):
        role = self.get_object()
        record_audit_log(request.user, "delete", role, before_data={"name": role.name}, after_data={})
        messages.success(request, "Role deleted successfully.")
        return super().delete(request, *args, **kwargs)


class FeatureListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = Feature
    template_name = "features/feature_list.html"
    context_object_name = "features"
    feature_code = "ROLE_MANAGEMENT"
    permission_action = "view"


class RolePermissionUpdateView(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = "roles/permission_form.html"
    feature_code = "ROLE_MANAGEMENT"
    permission_action = "update"

    def get_role(self):
        role = get_object_or_404(Role, pk=self.kwargs["pk"])
        if not self.request.user.is_superuser and (not hasattr(self.request.user, "profile") or role.organization != self.request.user.profile.organization):
            raise PermissionDenied
        return role

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        role = self.get_role()
        features = Feature.objects.all()
        permission_map = {
            permission.feature_id: permission
            for permission in RoleFeaturePermission.objects.filter(role=role)
        }
        context.update({
            "role": role,
            "features": features,
            "permission_map": permission_map,
        })
        return context

    def post(self, request, *args, **kwargs):
        role = self.get_role()

        before_permissions = [
            {
                "feature_id": str(permission.feature_id),
                "can_view": permission.can_view,
                "can_create": permission.can_create,
                "can_update": permission.can_update,
                "can_delete": permission.can_delete,
            }
            for permission in RoleFeaturePermission.objects.filter(role=role)
        ]
        features = Feature.objects.all()

        for feature in features:
            permission, _ = RoleFeaturePermission.objects.get_or_create(role=role, feature=feature)
            permission.can_view = bool(request.POST.get(f"view_{feature.id}"))
            permission.can_create = bool(request.POST.get(f"create_{feature.id}"))
            permission.can_update = bool(request.POST.get(f"update_{feature.id}"))
            permission.can_delete = bool(request.POST.get(f"delete_{feature.id}"))
            permission.save()

        record_audit_log(
            request.user,
            "update_permissions",
            role,
            before_data={"permissions": before_permissions},
            after_data={"role": role.name},
        )
        messages.success(request, "Role permissions updated successfully.")
        return redirect("role_list")
