from django.conf.urls.defaults import *
from models import StaffMember

staffmember_info = {'model': StaffMember}
queryset = StaffMember.objects.active()

urlpatterns = patterns('',
    url(r'^$',
        'index', 
        name='staff_index'),
    url(r'userinfo/(?P<user_id>[\d+])/$',
        'userinfo_ajax',
        name='staff_userinfo_ajax'),
    url(r'^(?P<slug>[^/]+)/$',
        'django.views.generic.list_detail.object_detail', 
        {'queryset': queryset, 'template': 'staff/staff_detail.html',},
        name='staff_staffmember_detail'),
    url(r'^(?P<slug>[^/]+)/contact/$',
        'contact',
        staffmember_info,
        name='staff_staffmember_contact'),
    url(r'^(?P<slug>[^/]+)/contact/done/$', 
        'contact_done', 
        staffmember_info, 
        name='staff_staffmember_contact_done'),
    url(r'^(?P<slug>[^/]+)/stories/$',
        'story_archive', 
        name='staff_staff_staffer_stories'),
)
