import rules
from . import predicates

# customer
rules.add_rule('create_customer', predicates.create_customer)

# job
rules.add_rule('create_job', predicates.create_job)

# cashflow
rules.add_rule('create_cashflow', predicates.create_cashflow)
rules.add_rule('create_cashflowtype', predicates.create_cashflowtype)
rules.add_rule('bank_cashflow', predicates.bank_cashflow)
