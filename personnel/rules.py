import rules
from . import predicates

rules.add_rule('is_ceo', predicates.is_ceo)
rules.add_rule('is_manager', predicates.is_manager)

rules.add_rule('create_new_user', predicates.create_new_user)
rules.add_rule('activate_deactivate_personnel_account', predicates.activate_deactivate_personnel_account)

rules.add_rule('view_personnel_index', predicates.view_personnel_index)
