from django.db import IntegrityError
from django.core.management.base import BaseCommand, CommandError
from personnel.models import Person, Personnel

class Command(BaseCommand):
    help = 'Create a superuser optionally passing an email and password'

    def add_arguments(self, parser):
        parser.add_argument('-email', type=str)
        parser.add_argument('-password', type=str)
        parser.add_argument('-fname', type=str)
        parser.add_argument('-lname', type=str)
        parser.add_argument('-display', type=str)

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Create superuser'))
        email = options['email'] if options['email'] else "orjichidi95@gmail.com"
        password = options['password'] if options['password'] else "dwarfstar"
        fname = options['fname'] if options['fname'] else "chidi"
        lname = options['lname'] if options['lname'] else "orji"
        display = options['display'] if options['password'] else "chidimo"

        try:
            su = Person.objects.create_user(email=email, password=password)
            su.is_superuser = True
            su.is_admin = True
            su.is_active = True
            su.save()
            self.stdout.write(self.style.SUCCESS(f'Superuser {email} created successfully'))
        except IntegrityError:
            su = Person.objects.get(email=email)
            self.stdout.write(self.style.ERROR(f'Superuser {email} already exists'))

        try:
            Personnel.objects.get_or_create(
                user=su,
                first_name=fname,
                last_name=lname,
                display_name=display,
            )
            self.stdout.write(self.style.SUCCESS(f'Personnel { display } created successfully'))
        except IntegrityError:
            self.stdout.write(self.style.ERROR(f'User { display } already exists'))
