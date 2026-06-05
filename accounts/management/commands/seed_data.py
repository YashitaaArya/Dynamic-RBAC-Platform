from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction

from audit_logs.services import record_audit_log
from organizations.models import Organization
from roles.models import Feature, Role, RoleFeaturePermission
from accounts.models import UserProfile


class Command(BaseCommand):
    help = "Seed initial organizations, features, roles, users, and permissions."

    def handle(self, *args, **options):
        with transaction.atomic():
            self.stdout.write("Seeding organizations...")
            organizations = [
                {"name": "Acme Corporation", "description": "Sample organization for platform admins."},
                {"name": "Nova Ventures", "description": "Secondary organization for tenant isolation."},
            ]
            org_map = {}
            for org_data in organizations:
                org, created = Organization.objects.get_or_create(name=org_data["name"], defaults={"description": org_data["description"]})
                org_map[org.name] = org
                if created:
                    self.stdout.write(f"Created organization: {org.name}")

            self.stdout.write("Seeding features...")
            feature_items = [
                {"name": "Dashboard", "code": "DASHBOARD", "description": "Access the main dashboard."},
                {"name": "User Management", "code": "USER_MANAGEMENT", "description": "Manage user profiles and roles."},
                {"name": "Organization Management", "code": "ORG_MANAGEMENT", "description": "Manage organizations."},
                {"name": "Role Management", "code": "ROLE_MANAGEMENT", "description": "Manage roles and feature permissions."},
                {"name": "Audit Logs", "code": "AUDIT_LOGS", "description": "View audit trail and system changes."},
            ]
            feature_map = {}
            for feature_data in feature_items:
                feature, created = Feature.objects.get_or_create(code=feature_data["code"], defaults={"name": feature_data["name"], "description": feature_data["description"]})
                feature_map[feature.code] = feature
                if created:
                    self.stdout.write(f"Created feature: {feature.code}")

            self.stdout.write("Seeding default roles...")
            default_roles = ["Super Admin", "Organization Admin", "Manager", "Employee"]
            role_map = {}
            for org in org_map.values():
                for name in default_roles:
                    role, created = Role.objects.get_or_create(
                        organization=org,
                        name=name,
                        defaults={"description": f"Default role for {name} in {org.name}", "is_default": True},
                    )
                    role_map[(org.name, name)] = role
                    if created:
                        self.stdout.write(f"Created role: {role.name} for {org.name}")

            self.stdout.write("Seeding permission mappings...")
            permission_default = {
                "Super Admin": {"view": True, "create": True, "update": True, "delete": True},
                "Organization Admin": {"view": True, "create": True, "update": True, "delete": True},
                "Manager": {"view": True, "create": False, "update": False, "delete": False},
                "Employee": {"view": True, "create": False, "update": False, "delete": False},
            }

            for org in org_map.values():
                for role_name, permission_config in permission_default.items():
                    role = role_map[(org.name, role_name)]
                    for feature in feature_map.values():
                        RoleFeaturePermission.objects.update_or_create(
                            role=role,
                            feature=feature,
                            defaults={
                                "can_view": permission_config["view"],
                                "can_create": permission_config["create"],
                                "can_update": permission_config["update"],
                                "can_delete": permission_config["delete"],
                            },
                        )

            self.stdout.write("Seeding users...")
            users = [
                {
                    "username": "superadmin",
                    "email": "superadmin@acme.local",
                    "first_name": "Super",
                    "last_name": "Admin",
                    "password": "SuperAdmin123!",
                    "organization": org_map["Acme Corporation"],
                    "role": role_map[("Acme Corporation", "Super Admin")],
                    "is_staff": True,
                    "is_superuser": True,
                },
                {
                    "username": "orgadmin",
                    "email": "orgadmin@acme.local",
                    "first_name": "Org",
                    "last_name": "Admin",
                    "password": "OrgAdmin123!",
                    "organization": org_map["Acme Corporation"],
                    "role": role_map[("Acme Corporation", "Organization Admin")],
                    "is_staff": True,
                    "is_superuser": False,
                },
                {
                    "username": "manager",
                    "email": "manager@acme.local",
                    "first_name": "Team",
                    "last_name": "Manager",
                    "password": "Manager123!",
                    "organization": org_map["Acme Corporation"],
                    "role": role_map[("Acme Corporation", "Manager")],
                    "is_staff": False,
                    "is_superuser": False,
                },
                {
                    "username": "employee",
                    "email": "employee@nova.local",
                    "first_name": "Regular",
                    "last_name": "Employee",
                    "password": "Employee123!",
                    "organization": org_map["Nova Ventures"],
                    "role": role_map[("Nova Ventures", "Employee")],
                    "is_staff": False,
                    "is_superuser": False,
                },
            ]

            for user_data in users:
                user, created = User.objects.get_or_create(username=user_data["username"], defaults={
                    "email": user_data["email"],
                    "first_name": user_data["first_name"],
                    "last_name": user_data["last_name"],
                    "is_staff": user_data["is_staff"],
                    "is_superuser": user_data["is_superuser"],
                })
                if created:
                    user.set_password(user_data["password"])
                    user.save()
                    UserProfile.objects.create(
                        user=user,
                        organization=user_data["organization"],
                        role=user_data["role"],
                        is_active=True,
                    )
                    self.stdout.write(f"Created user: {user.username}")
                else:
                    profile, _ = UserProfile.objects.get_or_create(user=user, defaults={
                        "organization": user_data["organization"],
                        "role": user_data["role"],
                        "is_active": True,
                    })
                    if profile.role != user_data["role"]:
                        profile.role = user_data["role"]
                        profile.save()

            self.stdout.write(self.style.SUCCESS("Seed data completed."))
