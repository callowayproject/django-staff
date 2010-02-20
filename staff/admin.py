from models import StaffMember
from django.contrib import admin
from forms import StaffMemberForm
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

class StaffMemberAdmin(admin.StackedInline):
    form = StaffMemberForm
    fieldsets = (
        (None, {'fields': ('user',)}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'slug', 'bio', 'photo', 'is_active')}),
        ('Contact info', {'fields': ('email', 'phone')}),
        ('Responsibilities', {'fields': ('sites',)}),
    )
    raw_id_fields = ('user',)
    list_display = ('first_name', 'last_name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('first_name', 'last_name', 'slug')
    prepopulated_fields = {'slug': ('first_name','last_name')}
    filter_horizontal = ('sites',)
    model = StaffMember
    max_num = 1

class StaffUserAdmin(UserAdmin):
    inlines = [StaffMemberAdmin,]

#admin.site.register(StaffMember, StaffMemberAdmin)
admin.site.unregister(User)
admin.site.register(User, StaffUserAdmin)