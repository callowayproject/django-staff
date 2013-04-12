from django.conf.urls.defaults import patterns, url
from django.views.generic import TemplateView, DetailView
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
        TemplateView.as_view(template_name='staffmembers/contact_done.html'),
        name='staff_staffmember_contact_done'),
    url(r'^(?P<slug>[^/]+)/stories/$',
        'story_archive',
        name='staff_staff_staffer_stories'),
)

urlpatterns += patterns('',
    url(r'^(?P<slug>[^/]+)/$',
        DetailView.as_view(queryset=QUERYSET, template_name='staffmembers/details.html'),
        name='staff_staffmember_detail'),
)
