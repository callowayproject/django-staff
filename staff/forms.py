from django import forms
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from models import StaffMember

USE_TINYMCE = getattr(settings, 'STAFF_USE_TINYMCE', True)
if 'tinymce' in settings.INSTALLED_APPS and USE_TINYMCE:
    from tinymce.widgets import TinyMCE
    WIDGET = TinyMCE(attrs={'cols': 80, 'rows': 30})
else:
    WIDGET = forms.Textarea()

class StaffMemberForm(forms.ModelForm):
    """
    Basic form for entering data about the staff member. Changes the bio
    field to a tinyMCE widget if specified.
    """
    bio = forms.CharField(widget=WIDGET)
    
    class Meta:
        model = StaffMember
        exclude = ('slug', 'first_name', 'last_name')


class ContactForm(forms.Form):
    """
    A simple contact form to allow contacting the staff
    """
    name = forms.CharField(label=_('Your Name'))
    email = forms.EmailField(label=_('Your Email'))
    message = forms.CharField(label=_('Message'), widget=forms.Textarea)