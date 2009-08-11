from django import forms
from django.utils.translation import ugettext_lazy as _

class ContactForm(forms.Form):
    name = forms.CharField(label=_('Your Name'))
    email = forms.EmailField(label=_('Your Email'))
    message = forms.CharField(label=_('Message'), widget=forms.Textarea)