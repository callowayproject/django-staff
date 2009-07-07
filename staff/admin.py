from models import StaffMember
from django.contrib import admin

class StaffMemberAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('user',)}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'bio', 'photo', 'show_photo', 'is_active')}),
        ('Contact info', {'fields': ('email', 'phone')}),
        ('Responsibilities', {'fields': ('sites',)}),
    )
    list_display = ('first_name', 'last_name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('first_name', 'last_name', 'slug')
    prepopulated_fields = {'slug': ('first_name','last_name')}
    filter_horizontal = ('sites',)

admin.site.register(StaffMember, StaffMemberAdmin)
