from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from stdimage.models import StdImageField
from typing import List
from django.template.defaultfilters import slugify
from django.contrib.auth import get_user_model


class UserManage(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email or not password:
            raise ValueError("E-mail e senha são obrigatórios")

        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("superuser precisa ser True")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("staff precisa ser True")

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    datetime_created = models.DateTimeField("Data de criação ", auto_now_add=True)
    email = models.EmailField(unique=True, db_index=True)
    name = models.CharField(max_length=155)
    nickname = models.CharField(max_length=75)
    cpf = models.CharField(max_length=14, unique=True)
    fone = models.CharField(max_length=19, default="", blank=False)
    birth_date = models.DateField(null=True, blank=True)
    photo = StdImageField("photo user", upload_to='users', blank=True)
    slug = models.SlugField('Slug', max_length=150, blank=True, editable=False)
    money = models.DecimalField(max_digits=7, decimal_places=2, default=0, blank=True)
    bonus = models.DecimalField(max_digits=7, decimal_places=2, default=10.0, blank=True)
    

    USERNAME_FIELD: str = 'email'
    REQUIRED_FIELDS: List[str] = ['name', 'cpf']

    objects = UserManage()

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


def user_pre_save(signal, instance, sender, **kwargs):
    instance.slug = slugify(instance.name)


models.signals.pre_save.connect(user_pre_save, sender=get_user_model())
