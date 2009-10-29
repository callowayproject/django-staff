from django import forms
from django.utils.translation import ugettext_lazy as _
from models import StaffMember
from tinymce.widgets import TinyMCE

class StaffMemberForm(forms.ModelForm):
    bio = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    class Meta:
        model = StaffMember
        
class ContactForm(forms.Form):
    name = forms.CharField(label=_('Your Name'))
    email = forms.EmailField(label=_('Your Email'))
    message = forms.CharField(label=_('Message'), widget=forms.Textarea)