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
