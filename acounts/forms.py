from django import forms
from django.core import validators
from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError
from django.utils.text import capfirst
from django.utils.regex_helper import _lazy_re_compile
from django.utils.translation import gettext_lazy as _
from django.forms.widgets import TextInput


User = get_user_model()

class EmployeeNumberField(forms.IntegerField):
    widget = TextInput
    default_error_messages = {
        "invalid": _("社員番号は半角数字のみの入力です"),
    }
    #数字のみを判定するregex
    default_validators = [validators.RegexValidator(regex=r'^[0-9]{6}$')]

    #validatorを追加
    def __init__(self):
        self.validators = [self.default_validators, validators]
        super().__init__()

    def widget_attrs(self, widget):
        return {
            **super().widget_attrs(widget),
            "autocapitalize": "none",
            "autocomplete": "employee_number",
            "autofocus": True,
        }


class CustomAuthenticationForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """

    employee_number = EmployeeNumberField()
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )

    error_messages = {
        "invalid_login": _(
            "Please enter a correct %(employee_number)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        "inactive": _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        # Set the max length and label for the "employee_number" field.
        self.employee_number_field = User._meta.get_field(User.USERNAME_FIELD)
        employee_number_max_length = 6
        self.fields["employee_number"].max_length = employee_number_max_length
        self.fields["employee_number"].widget.attrs["maxlength"] = employee_number_max_length
        if self.fields["employee_number"].label is None:
            self.fields["employee_number"].label = capfirst(self.employee_number_field.verbose_name)

    def clean(self):
        employee_number = self.cleaned_data.get("employee_number")
        password = self.cleaned_data.get("password")

        if employee_number is not None and password:
            self.user_cache = authenticate(
                self.request, employee_number=employee_number, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``ValidationError``.

        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise ValidationError(
                self.error_messages["inactive"],
                code="inactive",
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages["invalid_login"],
            code="invalid_login",
            params={"employee_number": self.employee_number_field.verbose_name},
        )


class LoginForm(CustomAuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        field_classes = ('bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500')
        
        for field in self.fields.values():
            #全てのフォームの部品にplaceholderを定義して、入力フォームにフォーム名が表示されるように指定する
            field.widget.attrs['placeholder'] = field.label
            #classを追加
            field.widget.attrs['class'] = field_classes
