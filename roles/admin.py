from django.contrib import admin

from .models import Feature, Role, RoleFeaturePermission


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name", "organization", "is_default", "created_at")
    list_filter = ("organization", "is_default")
    search_fields = ("name", "description")


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "description", "created_at")
    search_fields = ("name", "code", "description")


@admin.register(RoleFeaturePermission)
class RoleFeaturePermissionAdmin(admin.ModelAdmin):
    list_display = ("role", "feature", "can_view", "can_create", "can_update", "can_delete")
    list_filter = ("can_view", "can_create", "can_update", "can_delete")
    search_fields = ("role__name", "feature__name", "feature__code")
