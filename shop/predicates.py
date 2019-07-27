from rules import predicate

def user_permissions(user):
    return [each.code_name for each in user.personnel.personnelpermission_set.all()]

# customer
@predicate
def create_customer(user):
    return 'create_customer' in user_permissions(user)

@predicate
def edit_customer(user):
    return 'edit_customer' in user_permissions(user)

# job
@predicate
def create_job(user):
    return 'create_job' in user_permissions(user)

@predicate
def edit_job(user):
    return 'edit_job' in user_permissions(user)

@predicate
def mark_accepted(user):
    return 'mark_accepted' in user_permissions(user)

# cashflow
@predicate
def create_cashflow(user):
    return 'create_cashflow' in user_permissions(user)

@predicate
def create_cashflowtype(user):
    return 'create_cashflowtype' in user_permissions(user)

@predicate
def bank_cashflow(user):
    return 'bank_cashflow' in user_permissions(user)
