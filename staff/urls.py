from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import direct_to_template
from models import StaffMember

STAFFMEMBER_INFO = {'model': StaffMember}
QUERYSET = StaffMember.objects.active()

urlpatterns = patterns('staff.views',
    url(r'^$',
        'index',
        name='staff_index'),
    url(r'userinfo/(?P<user_id>[\d+])/$',
        'userinfo_json',
        name='staff_userinfo_json'),
    url(r'^(?P<slug>[^/]+)/contact/$',
        'contact',
        name='staff_staffmember_contact'),
    url(r'^contact/done/$',
        direct_to_template,
        {'template': 'staffmembers/contact_done.html'},
        name='staff_staffmember_contact_done'),
    url(r'^(?P<slug>[^/]+)/stories/$',
        'story_archive',
        name='staff_staff_staffer_stories'),
)

urlpatterns += patterns('',
    url(r'^(?P<slug>[^/]+)/$',
        'django.views.generic.list_detail.object_detail',
        {'queryset': QUERYSET, 'template_name': 'staffmembers/details.html', },
        name='staff_staffmember_detail'),
)
