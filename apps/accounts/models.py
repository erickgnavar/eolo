from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=CustomUserManager.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):

    USERNAME_FIELD = 'email'

    ROLE_CHOICES = (
        ('ADMINISTRATOR', _('Administrator')),
        ('USER', _('User'))
    )

    objects = CustomUserManager()

    email = models.EmailField(
        _('Email'),
        unique=True,
        max_length=255,
        db_index=True
    )

    first_name = models.CharField(
        _('First Name'),
        max_length=50
    )
    last_name = models.CharField(
        _('Last Name'),
        max_length=50
    )
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    role = models.CharField(
        _('Role'),
        max_length=50,
        default='USER',
        choices=ROLE_CHOICES
    )

    def get_full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def get_short_name(self):
        return self.email

    def __unicode__(self):
        return self.email

    @classmethod
    def make_random_password(cls):
        from uuid import uuid4
        return uuid4().hex
