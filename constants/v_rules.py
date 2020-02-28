from shop.rules import SHOP_RULES
from personnel.rules import PERSONNEL_RULES
from account.rules import ACCOUNT_RULES

PERMS = [
    ('shop', SHOP_RULES),
    ('account', ACCOUNT_RULES),
    ('personnel', PERSONNEL_RULES),
]
APP_RULES = [(e[0], code_name, name) for e in PERMS for code_name, name in e[1].items()]

RULES_CODE_NAMES = [each[1] for each in APP_RULES]
