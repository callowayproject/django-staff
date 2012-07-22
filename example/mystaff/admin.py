from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from staff.admin import StaffMemberAdmin

from .models import MyStaffMember


class MyStaffMemberAdmin(StaffMemberAdmin):
    fieldsets = (
        ('Personal Info', {'fields': ('bio', 'photo', 'website', 'phone',)}),
        ('Social Media', {'fields': ('github','twitter', 'facebook', 'google_plus')}),
        ('Responsibilities', {'fields': ('sites',)}),
    )
    model = MyStaffMember

class MyStaffUserAdmin(UserAdmin):
    """
    Subclasses the UserAdmin to add the staffmember as an inline.
    """
    inlines = [MyStaffMemberAdmin, ]

admin.site.unregister(User)
admin.site.register(User, MyStaffUserAdmin)
