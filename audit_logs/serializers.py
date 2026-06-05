from rest_framework import serializers

from .models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.username", read_only=True)
    organization_name = serializers.CharField(source="organization.name", read_only=True)

    class Meta:
        model = AuditLog
        fields = (
            "id",
            "user_name",
            "organization_name",
            "action",
            "model_name",
            "object_id",
            "before_data",
            "after_data",
            "timestamp",
        )
