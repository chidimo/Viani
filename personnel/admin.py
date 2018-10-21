"""Admin"""

from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import (
    PersonChangeForm, PersonCreationForm,
    )
from .models import Person, Designation, Personnel, PersonnelPermission

class GroupAdmin(admin.ModelAdmin):
    list_display = ("name", "all_users")

    def all_users(self, obj):
        return ", ".join([p.personnel.display_name for p in obj.user_set.all()])

    def all_permissions(self, obj):
        return ", ".join([p.name for p in obj.permissions.all()])

class PersonnelAdmin(admin.ModelAdmin):
    list_display = ("__str__",  "personnel_groups", "personnel_permissions", "display_name", "first_name", "last_name", "status", "designation",
        "address", 'avatar' )
    search_fields = ("display_name", "first_name", "last_name")
    list_select_related = True
    # list_editable = ('status', 'designation', 'balance')

class PersonAdmin(BaseUserAdmin):
    form = PersonChangeForm
    add_form = PersonCreationForm

    list_display = ('email', 'is_admin', "personnel", "is_active",)
    list_filter = ('is_admin', )
    fieldsets = (
        (None, {'fields' : ('email', 'password',)}),
        ('Personal info', {'fields' : ()}),
        ('Permissions', {'fields' : ('is_admin', 'is_active', 'is_superuser', 'groups',)}),
        ("Another set", {"fields" : ()})
    )

    add_fieldsets = (
        (None, {
            'classes' : ('wide', ),
            'fields' : ('email', 'password1', 'password2',)}
        ),
    )
    search_fields = ('email', )
    ordering = ('email', )
    filter_horizontal = ()

class PersonnelPermissionAdmin(admin.ModelAdmin):
    list_display = ("name", "code_name", "permitted_personnels")

admin.site.register(Personnel, PersonnelAdmin)
admin.site.register(PersonnelPermission, PersonnelPermissionAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Designation)

admin.site.unregister(Group)
admin.site.register(Permission)
admin.site.register(Group, GroupAdmin)
