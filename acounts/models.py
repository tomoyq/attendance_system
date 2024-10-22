from django.db import models
from django.core.validators import RegexValidator

from django.apps import apps
from django.contrib import auth
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.contrib.auth.hashers import make_password

from django.contrib.auth.validators import UnicodeUsernameValidator

from django.utils.translation import gettext_lazy as _

from work.models import Manager


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, employee_number, name, password, **extra_fields):
        """
        Create and save a user with the given name, email, and password.
        """
        if not name:
            raise ValueError("The given name must be set")
        if not employee_number:
            raise ValueError("The given employee_number must be set")
        
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        name = GlobalUserModel.normalize_username(name)
        user = self.model(name=name, employee_number=employee_number, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, employee_number, name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(employee_number, name, password, **extra_fields)

    def create_superuser(self, employee_number, name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(employee_number, name, password, **extra_fields)

    def with_perm(
        self, perm, is_active=True, include_superusers=True, backend=None, obj=None
    ):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    "You have multiple authentication backends configured and "
                    "therefore must provide the `backend` argument."
                )
        elif not isinstance(backend, str):
            raise TypeError(
                "backend must be a dotted import path string (got %r)." % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, "with_perm"):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """

    username_validator = UnicodeUsernameValidator()

    employee_number = models.CharField(
        primary_key=True,
        validators=[RegexValidator(r'^[0-9]{6}$')],
        error_messages={
            "unique": _("A user with that employee_number already exists."),
        },
        #管理者のログイン画面に社員番号と表示
        verbose_name="社員番号",
    )
    name = models.CharField(
        _("名前"),
        max_length=150,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
    )
    manager_id = models.ForeignKey(
        Manager,
        on_delete=models.CASCADE,
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    objects = CustomUserManager()

    EMAIL_FIELD = ""
    USERNAME_FIELD = "employee_number"
    REQUIRED_FIELDS = ["name","manager_id"]

    def __str__(self):
        return f'{str(self.employee_number)} {self.name}'

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    #def email_user(self, subject, message, from_email=None, **kwargs):
    #    """Send an email to this user."""
    #    send_mail(subject, message, from_email, [self.email], **kwargs)