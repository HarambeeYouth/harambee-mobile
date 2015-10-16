from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from my_auth.forms import HarambeeChangeForm, HarambeeCreationForm
from my_auth.models import Harambee


class HarambeeAdmin(UserAdmin):
    # The forms to add and change user instances
    form = HarambeeChangeForm
    add_form = HarambeeCreationForm
    list_max_show_all = 1000
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ("username", "first_name", "last_name", "lps")
    list_filter = ("first_name", "last_name", "mobile")
    search_fields = ("last_name", "first_name", "username")
    ordering = ("last_name", "first_name", "last_login")
    filter_horizontal = ()
    readonly_fields = ("mobile",)

    fieldsets = (
        ("Personal info", {"fields": ("first_name", "last_name",
                                      "email", "mobile", "lps")}),
        ("Access", {"fields": ("username", "password",
                               "is_active", "unique_token")}),
        ("Permissions", {"fields": ("is_staff", "is_superuser", "groups")}),
        ("Important dates", {"fields": ("last_login", "date_joined")})
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        ("Personal info", {"fields": ("first_name", "last_name", "lps")}),
        ("Access", {"fields": ("username", "password1",
                               "password2")}),
    )

admin.site.register(Harambee, HarambeeAdmin)