from django.core.management.base import BaseCommand
from personnel.models import PersonnelPermission

from constants.v_rules import RULES_CODE_NAMES

class Command(BaseCommand):
    help = 'Remove permissions that are not in permissions dictionary'

    def handle(self, *args, **options):
        count = 0
        self.stdout.write(self.style.SUCCESS('Start cleaning permissions'))
        existing_permissions = PersonnelPermission.objects.all()
        for perm in existing_permissions:
            if perm.code_name not in RULES_CODE_NAMES:
                self.stdout.write(self.style.ERROR(f'Delete permission {perm.name}'))
                perm.delete()
                count += 1
        self.stdout.write(self.style.SUCCESS(f'Deleted {count} permissions'))
