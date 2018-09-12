from django.core.management.base import BaseCommand #, CommandError
from personnel.models import Personnel, PersonnelPermission

class Command(BaseCommand):
    help = 'Grant all permissions to specified user'

    def add_arguments(self, parser):
        parser.add_argument('-email', type=str)

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Start granting permissions'))
        if options['email']:
            email = options['email']
        else:
            email = "orjichidi95@gmail.com"
        personnel = Personnel.objects.get(user__email=email)
        permissions = PersonnelPermission.objects.all()
        for perm in permissions:
            self.stdout.write(self.style.SUCCESS('User {}: Granting {}'.format(personnel, perm)))
            perm.personnel.add(personnel)
        self.stdout.write(self.style.SUCCESS('Finish granting permissions'))
