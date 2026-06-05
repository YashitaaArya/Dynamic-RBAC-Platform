from django import template

from permissions_app.utils import has_permission as permission_check

register = template.Library()


@register.simple_tag(takes_context=True)
def has_permission(context, feature_code, action="view"):
    request = context.get("request")
    if not request:
        return False
    return permission_check(request.user, feature_code, action)


@register.filter
def get_item(dictionary, key):
    if not dictionary:
        return None
    return dictionary.get(key)
