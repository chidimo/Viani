from rules import predicate

def user_permissions(user):
    return [each.code_name for each in user.personnel.personnelpermission_set.all()]

@predicate
def is_ceo(user):
    return 'ceo' in list(user.groups.values_list('name', flat=True))

@predicate
def is_manager(user):
    return 'manager' in list(user.groups.values_list('name', flat=True))

@predicate
def create_new_user(user):
    return 'create_new_user' in user_permissions(user)

@predicate
def activate_deactivate_personnel_account(user):
    return 'activate_deactivate_personnel_account' in user_permissions(user)

@predicate
def view_personnel_index(user):
    return 'view_personnel_index' in user_permissions(user)

@predicate
def view_permissions_index(user):
    return 'view_permission_index' in user_permissions(user)

@predicate
def view_group_index(user):
    return 'view_group_index' in user_permissions(user)

@predicate
def permission_grant(user):
    return 'permission_grant' in user_permissions(user)

@predicate
def permission_revoke(user):
    return 'permission_revoke' in user_permissions(user)

@predicate
def group_add_personnel(user):
    return 'group_add_personnel' in user_permissions(user)

@predicate
def group_remove_personnel(user):
    return 'group_remove_personnel' in user_permissions(user)

@predicate
def grant_multiple_permissions(user):
    return 'grant_multiple_permissions' in user_permissions(user)

