from rules import predicate

def user_permissions(user):
    return [each.code_name for each in user.personnel.personnelpermission_set.all()]

@predicate
def create_new_job(user):
    return 'create_new_job' in user_permissions(user)
