from django.contrib.auth.models import User
from rest_framework import serializers

from organizations.models import Organization
from roles.models import Role
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    organization = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all())
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = UserProfile
        fields = ("organization", "role", "is_active")


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "password", "profile")
        read_only_fields = ("id",)

    def create(self, validated_data):
        profile_data = validated_data.pop("profile")
        password = validated_data.pop("password", None)
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        UserProfile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", {})
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        profile = instance.profile
        for attr, value in profile_data.items():
            setattr(profile, attr, value)
        profile.save()
        return instance


class UserListSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source="profile.role.name", read_only=True)
    organization = serializers.CharField(source="profile.organization.name", read_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "role", "organization")
