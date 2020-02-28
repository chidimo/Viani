"""Models"""

import uuid
from decimal import Decimal

from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.core.validators import RegexValidator
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

from sorl.thumbnail import ImageField

from .utils.models import TimeStampedModel
from .utils.fields import AutoMultipleSlugField
from .utils.media_handlers import upload_avatar

from constants.validators import validate_phone

class PersonManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("You must provide an email address")
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user

class Person(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True, verbose_name='email address')
    join_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = PersonManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return "User: {}".format(self.email)

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        try:
            return self.personnel == obj.personnel
        except AttributeError:
            if self.is_admin:
                return True

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def personnel(self):
        return self.personnel.display_name

class Designation(TimeStampedModel):
    designation = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('designation', )

    def __str__(self):
        return self.designation

    def get_absolute_url(self):
        return reverse('personnel:designations')

class Personnel(TimeStampedModel):
    ML = "MALE"
    FM = 'FEMALE'
    AC = 'ACTIVE'
    IN = 'INACTIVE'
    SS = 'SUSPENDED'
    sex_choices = ((ML, 'male'), (FM, 'female'))
    status_choices = ((AC, 'active'), (IN, 'inactive'), (SS, 'suspended'))

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=12, choices=status_choices, default='active')
    designation = models.ForeignKey(Designation, null=True, on_delete=models.SET_NULL)

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    dob = models.DateField(default=timezone.now)
    sex = models.CharField(max_length=10, choices=sex_choices, default='male')
    display_name = models.CharField(max_length=25, unique=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    avatar = ImageField(upload_to=upload_avatar, null=True, blank=True)

    slug = AutoMultipleSlugField(set_using=["last_name", "first_name"], max_length=255)
    phone = models.CharField(max_length=15, null=True, blank=True, unique=True, validators=[validate_phone])

    class Meta:
        ordering = ['display_name']
        verbose_name_plural = 'personnels'

    def __str__(self):
        return self.display_name

    def get_absolute_url(self):
        return reverse('personnel:index')

    def get_edit_url(self):
        return reverse('personnel:edit', kwargs={'pk' : self.id, 'slug' : self.slug})

    def get_user_creation_url(self):
        return reverse('personnel:personnel_new_activate', kwargs={'pk' : self.id, 'slug' : self.slug})

    def get_user_join_success_url(self):
        return reverse("personnel:personnel_new_success", args=[str(self.display_name)])

    def personnel_permissions(self):
        return ", ".join([each.code_name for each in self.personnelpermission_set.all()])

    @property
    def personnel_groups(self):
        return ", ".join(list(self.user.groups.values_list('name', flat=True)))

class PersonnelPermission(TimeStampedModel):
    name = models.CharField(max_length=50)
    code_name = models.CharField(max_length=50, unique=True)
    app_name = models.CharField(max_length=25, default='')
    personnel = models.ManyToManyField(Personnel)

    class Meta:
        ordering = ('app_name', "name", )

    def __str__(self):
        return self.code_name

    @property
    def permitted_personnels(self):
        return ", ".join([personnel.display_name for personnel in self.personnel.all()])
