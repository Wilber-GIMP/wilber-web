from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.users.models import User
from apps.users.models import UserProfile


class ProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "Profile"
    fk_name = "user"
    readonly_fields = ("birthday",)


class CustomUserAdmin(UserAdmin):
    # inlines = (ProfileInline, )

    list_display = ("username", "email", "name", "is_staff")
    search_fields = ("username", "name", "email")

    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("name",)}),)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "email")

    readonly_fields = ("email",)

    # fields = ('user', 'name', 'email')

    def email(self, obj):
        return obj.user.email

    def name(self, obj):
        return obj.user.get_full_name()


admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
