from django.core.management.base import BaseCommand
from personnel.models import Personnel, PersonnelPermission

common_permissions = [
    'create_expenditure',
]


class Command(BaseCommand):
    help = 'Grant all permissions to specified user'

    def add_arguments(self, parser):
        parser.add_argument('-email', type=str)

    def handle(self, *args, **options):

        self.stdout.write(self.style.SUCCESS(
            'Start granting common permissions to all users'))
        personnels = Personnel.objects.filter(user__is_active=True)
        # permissions = PersonnelPermission.objects.all()

        for each in common_permissions:
            perm = PersonnelPermission.objects.get(code_name=each)
            self.stdout.write(self.style.SUCCESS(f'{perm.name.title()}'))
            for pers in personnels:
                perm.personnel.add(pers)
                self.stdout.write(self.style.SUCCESS(
                    f'\t{pers} granted'))
            self.stdout.write(self.style.SUCCESS('\n*********************\n'))
        self.stdout.write(self.style.SUCCESS(
            'Finish granting common permissions to all users'))
