from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _


# Register your models here.

User = get_user_model()

#カスタムユーザーモデルを管理サイトで管理する場合useradminのサブクラスをregister関数の引数に渡す
#useradminのfieldをカスタムユーザーモデルに合わせる必要がある
class CustumUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("employee_number", "password")}),
        (_("Personal info"), {"fields": ("name",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("employee_number", "usable_password", "password1", "password2", "name", "manager_id"),
            },
        ),
    )
    list_display = ("employee_number", "name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("employee_number", "name", "manager_id",)
    ordering = ("employee_number",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )


admin.site.register(User, CustumUserAdmin)