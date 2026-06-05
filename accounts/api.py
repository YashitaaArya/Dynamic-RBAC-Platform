from django.contrib.auth.models import User
from rest_framework import mixins, viewsets

from audit_logs.services import record_audit_log
from .serializers import UserSerializer, UserListSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.select_related("profile")
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return User.objects.select_related("profile")
        if hasattr(user, "profile") and user.profile.organization:
            return User.objects.filter(profile__organization=user.profile.organization).select_related("profile")
        return User.objects.none()

    def perform_create(self, serializer):
        instance = serializer.save()
        record_audit_log(
            self.request.user,
            action="create",
            instance=instance,
            before_data={},
            after_data=instance.username,
        )

    def perform_update(self, serializer):
        instance = serializer.instance
        before_data = {
            "username": instance.username,
            "email": instance.email,
            "first_name": instance.first_name,
            "last_name": instance.last_name,
        }
        updated_instance = serializer.save()
        record_audit_log(
            self.request.user,
            action="update",
            instance=updated_instance,
            before_data=before_data,
            after_data=updated_instance.username,
        )

    def get_serializer_class(self):
        if self.action == "list":
            return UserListSerializer
        return UserSerializer
