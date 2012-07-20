from django import forms
from django.utils.translation import ugettext_lazy as _

from models import StaffMember


class StaffMemberForm(forms.ModelForm):
    """
    Basic form for entering data about the staff member. Changes the bio
    field to a tinyMCE widget if specified.
    """
    # bio = forms.CharField(widget=WIDGET)

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
