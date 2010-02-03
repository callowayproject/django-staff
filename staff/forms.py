from django import forms
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from models import StaffMember
from tinymce.widgets import TinyMCE

if 'tinymce' in settings.INSTALLED_APPS:
    from tinymce.widgets import TinyMCE
    widget = TinyMCE(attrs={'cols': 80, 'rows': 30})
else:
    widget = forms.Textarea()
    
class StaffMemberForm(forms.ModelForm):
    bio = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    class Meta:
        model = StaffMember
        
class ContactForm(forms.Form):
    name = forms.CharField(label=_('Your Name'))
    email = forms.EmailField(label=_('Your Email'))
    message = forms.CharField(label=_('Message'), widget=forms.Textarea)