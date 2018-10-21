from django.core.management.base import BaseCommand#, CommandError
from personnel.models import PersonnelPermission

perms = {}

perms['create_new_user'] = 'Can create a new user'
perms['activate_deactivate_personnel_account'] = 'Can activate or deactivate a user'

perms['create_new_job'] = 'Can create a new job'

class Command(BaseCommand):
    help = 'Create all permissions'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Start creating permissions'))
        for key, value in perms.items():
            PersonnelPermission.objects.get_or_create(name=value.strip(), code_name=key.strip())
            self.stdout.write(key)
        self.stdout.write(self.style.SUCCESS('Finish creating permissions'))
