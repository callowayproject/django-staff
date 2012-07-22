from datetime import datetime

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils import simplejson
from django.core.mail import EmailMessage

from staff.models import StaffMember
from staff.forms import ContactForm


def index(request, template_name='staffmembers/index.html'):
    """
    The list of employees or staff members
    """
    return render_to_response(template_name,
                              {'staff': StaffMember.objects.active()},
                              context_instance=RequestContext(request))


def userinfo_json(request, user_id):
    """
    Return the user's information in a json object
    """
    data = {'first_name': '',
            'last_name': '',
            'email': '',
            'slug': '',
            'bio': '',
            'phone': '',
            'is_active': False}

    try:
        member = StaffMember.objects.get(pk=user_id)
        for key in data.keys():
            if hasattr(member, key):
                data[key] = getattr(member, key, '')

    except StaffMember.DoesNotExist:
        pass

    return HttpResponse(simplejson.dumps(data),
                        mimetype='application/json')


def contact(request, slug, template_name='staffmembers/contact.html',
    success_url='/staff/contact/done/',
    email_subject_template='staffmembers/emails/subject.txt',
    email_body_template='staffmembers/emails/body.txt'):
    """
    Handle a contact request
    """
    member = get_object_or_404(StaffMember, slug__iexact=slug, is_active=True)

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = render_to_string(
                email_subject_template,
                {'member': member}
            )
            subject = ''.join(subject.splitlines())

            message = render_to_string(
                email_body_template,
                {'name': form.cleaned_data['name'],
                'email': form.cleaned_data['email'],
                'message': form.cleaned_data['message']}
            )

            EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL,
                [member.email], headers={
                    'Reply-To': form.cleaned_data['email']
            }).send()

            return HttpResponseRedirect(success_url)
    else:
        initial = {}
        if not request.user.is_anonymous():
            initial = {'name': '%s %s' % (
                            request.user.first_name, request.user.last_name),
                       'email': request.user.email}
        form = ContactForm(initial=initial)

    return render_to_response(template_name,
                              {'form': form,
                               'member': member},
                              context_instance=RequestContext(request))

# TODO: This needs to be refactored so that any other model can be referenced
def story_archive(request, slug, template_name='staffmembers/story_archive.html'):
    """
    Return the list of stories written by this staff member
    """
    member = get_object_or_404(StaffMember, slug__iexact=slug, is_active=True)

    stories = []
    if hasattr(member, 'story_set'):
        from story.settings import PUBLISHED_STATUS
        stories = member.story_set.filter(publish_date__lte=datetime.now()
            ).filter(status__exact=PUBLISHED_STATUS
            ).order_by('-publish_date')

    return render_to_response(template_name,
                              {'member': member,
                               'stories': stories},
                              context_instance=RequestContext(request))
