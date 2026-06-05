from roles.models import Feature, RoleFeaturePermission


ACTION_MAP = {
    "list": "view",
    "retrieve": "view",
    "create": "create",
    "update": "update",
    "partial_update": "update",
    "destroy": "delete",
}


def resolve_action(action: str) -> str:
    return ACTION_MAP.get(action, action)


def has_permission(user, feature_code: str, action: str) -> bool:
    if not user or not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    if not hasattr(user, "profile"):
        return False
    action = resolve_action(action)
    try:
        feature = Feature.objects.get(code=feature_code)
        permission = RoleFeaturePermission.objects.filter(role=user.profile.role, feature=feature).first()
    except Feature.DoesNotExist:
        return False
    if not permission:
        return False
    return getattr(permission, f"can_{action}", False)
