from django.core.management.base import BaseCommand
from personnel.models import PersonnelPermission

from constants.v_rules import APP_RULES

class Command(BaseCommand):
    help = 'Create all permissions'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Start creating permissions'))
        for each in APP_RULES:
            app_name = each[0]
            code_name = each[1]
            name = each[2]
            obj, _ = PersonnelPermission.objects.get_or_create(code_name=code_name.strip())
            obj.app_name = app_name.strip().lower()
            obj.name = name.strip().lower()
            obj.save()
            self.stdout.write(code_name)
        self.stdout.write(self.style.SUCCESS('Finish creating permissions'))
