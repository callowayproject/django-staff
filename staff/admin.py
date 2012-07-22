"""
Admin classes for the StaffMember model
"""
import django
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.forms.models import inlineformset_factory

# from staff.forms import StaffMemberForm
from staff.models import StaffMember

if django.VERSION[1] == 3:
    ADMIN_TEMPLATE = "admin/edit_inline/staff13.html"
else:
    ADMIN_TEMPLATE = "admin/edit_inline/staff.html"


class StaffMemberAdmin(admin.StackedInline):
    """
    Admin form for a StaffMember that won't appear if the associated User
    isn't actually a staff member.
    """
    # form = StaffMemberForm
    template = ADMIN_TEMPLATE
    fieldsets = (
        ('Personal Info', {'fields': ('bio', 'photo', 'website', 'phone',)}),
        ('Social Media', {'fields': ('twitter', 'facebook', 'google_plus')}),
        ('Responsibilities', {'fields': ('sites',)}),
    )
    filter_horizontal = ('sites',)
    model = StaffMember
    max_num = 1

    def get_formset(self, request, obj=None, **kwargs):
        """
        Return a form, if the obj has a staffmember object, otherwise
        return an empty form
        """
        if obj is not None and self.model.objects.filter(user=obj).count():
            return super(StaffMemberAdmin, self).get_formset(
                request,
                obj,
                **kwargs
            )

        defaults = {
            "exclude": None,
            "extra": 0,
            "max_num": 0,
        }
        return inlineformset_factory(self.parent_model, self.model, **defaults)


class StaffUserAdmin(UserAdmin):
    """
    Subclasses the UserAdmin to add the staffmember as an inline.
    """
    inlines = [StaffMemberAdmin, ]

admin.site.unregister(User)
admin.site.register(User, StaffUserAdmin)
