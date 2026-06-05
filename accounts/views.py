from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView

from audit_logs.services import record_audit_log
from permissions_app.mixins import PermissionRequiredMixin
from .forms import UserProfileForm, UserUpdateForm
from .models import UserProfile
from .serializers import UserSerializer


class AppLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = AuthenticationForm


class AppLogoutView(LogoutView):
    next_page = reverse_lazy("login")


class UserListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = UserProfile
    template_name = "users/user_list.html"
    context_object_name = "profiles"
    feature_code = "USER_MANAGEMENT"
    permission_action = "view"

    def get_queryset(self):
        user = self.request.user
        queryset = UserProfile.objects.select_related("user", "role", "organization")
        if user.is_superuser:
            return queryset
        if hasattr(user, "profile") and user.profile.organization:
            return queryset.filter(organization=user.profile.organization)
        return queryset.none()


class UserCreateView(PermissionRequiredMixin, LoginRequiredMixin, View):
    feature_code = "USER_MANAGEMENT"
    permission_action = "create"
    template_name = "users/user_form.html"

    def get(self, request):
        organization = request.user.profile.organization if hasattr(request.user, "profile") else None
        form = UserProfileForm(organization=organization)
        return render(request, self.template_name, {"form": form, "title": "Create User"})

    def post(self, request):
        organization = request.user.profile.organization if hasattr(request.user, "profile") else None
        form = UserProfileForm(request.POST, organization=organization)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create(
                username=data["username"],
                email=data["email"],
                first_name=data["first_name"],
                last_name=data["last_name"],
                is_active=data["is_active"],
            )
            password = data["password"]
            if password:
                user.set_password(password)
            else:
                user.set_unusable_password()
            user.save()
            profile = UserProfile.objects.create(
                user=user,
                organization=data["organization"],
                role=data["role"],
                is_active=data["is_active"],
            )
            record_audit_log(
                request.user,
                "create",
                profile,
                before_data={},
                after_data={"username": user.username, "organization": profile.organization.name, "role": profile.role.name},
            )
            messages.success(request, "User created successfully.")
            return redirect("user_list")
        return render(request, self.template_name, {"form": form, "title": "Create User"})


class UserUpdateView(PermissionRequiredMixin, LoginRequiredMixin, View):
    feature_code = "USER_MANAGEMENT"
    permission_action = "update"
    template_name = "users/user_form.html"

    def get_profile(self, request, pk):
        queryset = UserProfile.objects.select_related("user", "role", "organization")
        user = request.user
        if user.is_superuser:
            return get_object_or_404(queryset, user_id=pk)
        if hasattr(user, "profile") and user.profile.organization:
            return get_object_or_404(queryset.filter(organization=user.profile.organization), user_id=pk)
        raise PermissionDenied

    def get(self, request, pk):
        profile = self.get_profile(request, pk)
        form = UserUpdateForm(
            initial={
                "email": profile.user.email,
                "first_name": profile.user.first_name,
                "last_name": profile.user.last_name,
                "role": profile.role,
                "is_active": profile.is_active,
            },
            organization=profile.organization,
        )
        return render(request, self.template_name, {"form": form, "title": "Edit User", "profile": profile})

    def post(self, request, pk):
        profile = self.get_profile(request, pk)
        form = UserUpdateForm(request.POST, organization=profile.organization)
        if form.is_valid():
            data = form.cleaned_data
            user = profile.user
            before_data = {
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": profile.role.name,
                "is_active": profile.is_active,
            }
            user.email = data["email"]
            user.first_name = data["first_name"]
            user.last_name = data["last_name"]
            if data["password"]:
                user.set_password(data["password"])
            user.is_active = data["is_active"]
            user.save()
            profile.role = data["role"]
            profile.is_active = data["is_active"]
            profile.save()
            record_audit_log(
                request.user,
                "update",
                profile,
                before_data=before_data,
                after_data={"email": user.email, "role": profile.role.name, "is_active": profile.is_active},
            )
            messages.success(request, "User updated successfully.")
            return redirect("user_list")
        return render(request, self.template_name, {"form": form, "title": "Edit User", "profile": profile})
