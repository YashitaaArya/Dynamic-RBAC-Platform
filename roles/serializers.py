from rest_framework import serializers

from .models import Feature, Role, RoleFeaturePermission


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ("id", "name", "code", "description")


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ("id", "organization", "name", "description", "is_default", "created_by", "created_at", "updated_at")
        read_only_fields = ("created_by", "created_at", "updated_at")


class RoleFeaturePermissionSerializer(serializers.ModelSerializer):
    feature_name = serializers.CharField(source="feature.name", read_only=True)
    feature_code = serializers.CharField(source="feature.code", read_only=True)

    class Meta:
        model = RoleFeaturePermission
        fields = (
            "id",
            "role",
            "feature",
            "feature_name",
            "feature_code",
            "can_view",
            "can_create",
            "can_update",
            "can_delete",
            "updated_at",
        )
        read_only_fields = ("updated_at",)
