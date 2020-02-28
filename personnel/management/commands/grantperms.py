from django.core.management.base import BaseCommand
from personnel.models import Personnel, PersonnelPermission

eligible_emails = ('orjichidi95@gmail.com',
                   'damianorji@gmail.com', 'orjijude89@gmail.com')


class Command(BaseCommand):
    help = 'Grant all permissions to specified user'

    def add_arguments(self, parser):
        parser.add_argument('-email', type=str)

    def handle(self, *args, **options):
        email = options['email'] if options['email'] else "orjichidi95@gmail.com"
        if email not in eligible_emails:
            self.stdout.write(self.style.ERROR(
                'You are not eligible for blanket permissions'))
            return

        self.stdout.write(self.style.SUCCESS('Start granting permissions'))
        personnel = Personnel.objects.get(user__email=email)
        permissions = PersonnelPermission.objects.all()
        for perm in permissions:
            self.stdout.write(self.style.SUCCESS(
                f'{personnel} granted {perm.name.title()}'))
            perm.personnel.add(personnel)
        self.stdout.write(self.style.SUCCESS('Finish granting permissions'))
