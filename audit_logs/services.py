from django.forms.models import model_to_dict

from .models import AuditLog


def serialize_instance(instance):
    data = {}
    for field in instance._meta.fields:
        name = field.name
        value = getattr(instance, name)
        if field.is_relation:
            data[name] = str(value) if value is not None else None
        else:
            data[name] = value
    return data


def record_audit_log(user, action, instance=None, before_data=None, after_data=None):
    if before_data is None:
        before_data = {}
    if after_data is None:
        after_data = {}

    organization = None
    if instance is not None and hasattr(instance, "organization"):
        organization = getattr(instance, "organization")
    elif hasattr(user, "profile"):
        organization = user.profile.organization

    object_id = str(getattr(instance, "pk", "")) if instance is not None else ""
    model_name = instance._meta.model_name if instance is not None else "system"

    AuditLog.objects.create(
        user=user if user.is_authenticated else None,
        organization=organization,
        action=action,
        model_name=model_name,
        object_id=object_id,
        before_data=before_data,
        after_data=after_data,
    )
