from django.conf.urls.defaults import *
from models import StaffMember

staffmember_info = {'model': StaffMember}

urlpatterns = patterns('staff.views',
    url(r'^$',
        'index', 
        name='staff_index'),
    url(r'userinfo/(?P<user_id>[\d+])/$',
        'userinfo_ajax',
        name='staff_userinfo_ajax'),
    url(r'^(?P<slug>[^/]+)/$',
        'bio_page', 
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
        name='ellington_staff_staffer_stories'),
)
