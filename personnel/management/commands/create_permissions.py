from django.core.management.base import BaseCommand#, CommandError
from personnel.models import PersonnelPermission

perms = {}

perms['view_personnel_index'] = 'Can view personnel index'
perms['create_new_user'] = 'Can create a new user'
perms['activate_deactivate_personnel_account'] = 'Can activate or deactivate a user'

# customer
perms['create_customer'] = 'Can create customer'
perms['edit_customer'] = 'Can edit customer'

# job
perms['create_job'] = 'Can create job'
perms['edit_job'] = 'Can edit job'

# cashflow
perms['create_cashflow'] = 'Can create cashflow'
perms['create_cashflowtype'] = 'Can create cashflow type'
perms['bank_cashflow'] = 'Can bank cash'

class Command(BaseCommand):
    help = 'Create all permissions'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Start creating permissions'))
        for key, value in perms.items():
            PersonnelPermission.objects.get_or_create(name=value.strip(), code_name=key.strip())
            self.stdout.write(key)
        self.stdout.write(self.style.SUCCESS('Finish creating permissions'))
