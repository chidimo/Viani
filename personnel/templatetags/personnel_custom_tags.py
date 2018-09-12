from django import template

register = template.Library()

@register.filter()
def belongs_to(user, group_names):
    group_names = [name.strip() for name in group_names.split(",")]
    return user.groups.filter(name__in=group_names).count()
