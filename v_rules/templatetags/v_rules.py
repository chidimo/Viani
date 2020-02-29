from django import template

register = template.Library()

@register.simple_tag
def test_permission(perm, request, obj=None):
    # try:
    user_perms = request.user.personnel.personnel_permissions()
    return perm in user_perms
