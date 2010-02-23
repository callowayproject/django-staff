from models import StaffMember
from django.contrib import admin
from forms import StaffMemberForm
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

class StaffMemberAdmin(admin.StackedInline):
    form = StaffMemberForm
    fieldsets = (
        ('Personal Info', {'fields': ('bio', 'photo', 'is_active', 'phone',)}),
        ('Responsibilities', {'fields': ('sites',)}),
    )
    filter_horizontal = ('sites',)
    model = StaffMember
    max_num = 1

class StaffUserAdmin(UserAdmin):
    inlines = [StaffMemberAdmin,]

admin.site.unregister(User)
admin.site.register(User, StaffUserAdmin)