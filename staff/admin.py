from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.utils.functional import curry
from django.contrib.admin.util import flatten_fieldsets
from django.forms.models import inlineformset_factory

from staff.forms import StaffMemberForm
from staff.models import StaffMember

class StaffMemberAdmin(admin.StackedInline):
    # form = StaffMemberForm
    fieldsets = (
        ('Personal Info', {'fields': ('bio', 'photo', 'is_active', 'phone',)}),
        ('Responsibilities', {'fields': ('sites',)}),
    )
    filter_horizontal = ('sites',)
    model = StaffMember
    max_num = 1
    
    def get_formset(self, request, obj=None, **kwargs):
        """
        Return a form, if the obj is_staff, otherwise return an empty form
        """
        if obj is not None and obj.is_staff:
            return super(StaffMemberAdmin, self).get_formset(request, obj, **kwargs)
        
        defaults = {
            "exclude": None,
            "extra": 0,
            "max_num": 0,
        }
        return inlineformset_factory(self.parent_model, self.model, **defaults)

class StaffUserAdmin(UserAdmin):
    inlines = [StaffMemberAdmin,]

admin.site.unregister(User)
admin.site.register(User, StaffUserAdmin)