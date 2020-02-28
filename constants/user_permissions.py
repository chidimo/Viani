def user_permissions(user):
    return [each.code_name for each in user.personnel.personnelpermission_set.all()]
