from random import choice, randint, random

import django
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from personnel.models import Personnel

django.setup()

def superuser(
    email='orjichidi95@gmail.com',
    first_name="chidi",
    last_name="orji",
    phone="+2349036650603",
    display_name="dinma"):

    Person = get_user_model()

    try:
        su = Person.objects.create_user(email=email, password='dwarfstar')
        su.is_superuser = True
        su.is_admin = True
        su.is_active = True
        su.save()
    except IntegrityError: # email exists
        su = Person.objects.get(email=email)

    try:
        _ = Personnel.objects.get_or_create(
            user=su,
            first_name=first_name,
            last_name=last_name,
            display_name=display_name,
            phone=phone
            )
    except IntegrityError:
        pass

def handler(email, phone, display_name, first_name, last_name):
    Person = get_user_model()
    try:
        user = Person.objects.create_user(email=email, password='dwarfstar')
        user.is_active = True
        user.save()
    except IntegrityError:
        user = Person.objects.get(email=email)

    try:
        _ = Personnel.objects.get_or_create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            display_name=display_name,
            address="4 Adesuwa street",
            phone=phone
            )

    except IntegrityError:
        pass
