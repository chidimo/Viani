import rules
from . import predicates

# customer
rules.add_rule('create_customer', predicates.create_customer)
rules.add_rule('edit_customer', predicates.edit_customer)

# job
rules.add_rule('create_job', predicates.create_job)
rules.add_rule('edit_job', predicates.edit_job)
rules.add_rule('mark_accepted', predicates.mark_accepted)

# cashflow
rules.add_rule('create_cashflow', predicates.create_cashflow)
rules.add_rule('create_cashflowtype', predicates.create_cashflowtype)
rules.add_rule('bank_cashflow', predicates.bank_cashflow)
