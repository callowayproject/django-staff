from django import forms
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _

import os

URL_PREFIX = getattr(settings, 'STATIC_URL', settings.MEDIA_URL)

class DeleteCheckboxWidget(forms.CheckboxInput):
    def __init__(self, *args, **kwargs):
        self.is_image = kwargs.pop('is_image')
        self.value = kwargs.pop('initial')
        super(DeleteCheckboxWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        value = value or self.value
        if value:
            s = u'<label for="%s">%s %s</label>' % (
                    attrs['id'],
                    super(DeleteCheckboxWidget, self).render(name, False, attrs),
                    _('Delete')
                )
            if self.is_image:
                s += u'<br><img src="%s%s" width="50">' % (URL_PREFIX, value)
            else:
                s += u'<br><a href="%s%s">%s</a>' % (URL_PREFIX, value, os.path.basename(value))
            return s
        else:
            return u''
    
    def _has_changed(self, initial, data):
        return data


class RemovableFileFormWidget(forms.MultiWidget):
    def __init__(self, is_image=False, initial=None, **kwargs):
        widgets = (forms.FileInput(), DeleteCheckboxWidget(is_image=is_image, initial=initial))
        super(RemovableFileFormWidget, self).__init__(widgets)

    def decompress(self, value):
        return [None, value]


class RemovableFileFormField(forms.MultiValueField):
    widget = RemovableFileFormWidget
    field = forms.FileField
    is_image = False

    def __init__(self, *args, **kwargs):
        fields = [self.field(*args, **kwargs), forms.BooleanField(required=False)]
        # Compatibility with form_for_instance
        if kwargs.get('initial'):
            initial = kwargs['initial']
        else:
            initial = None
        self.widget = self.widget(is_image=self.is_image, initial=initial)
        super(RemovableFileFormField, self).__init__(fields, label=kwargs.pop('label'), required=False)

    def compress(self, data_list):
        return data_list


class RemovableImageFormField(RemovableFileFormField):
    field = forms.ImageField
    is_image = True


class RemovableFileField(models.FileField):
    def delete_file(self, instance, *args, **kwargs):
        if getattr(instance, self.attname):
            image = getattr(instance, '%s' % self.name)
            file_name = image.path
            # If the file exists and no other object of this type references it,
            # delete it from the filesystem.
            if os.path.exists(file_name) and \
                not instance.__class__._default_manager.filter(**{'%s__exact' % self.name: getattr(instance, self.attname)}).exclude(pk=instance._get_pk_val()):
                os.remove(file_name)

    def get_internal_type(self):
        return 'FileField'

    def save_form_data(self, instance, data):
        if data and data[0]: # Replace file
            self.delete_file(instance)
            super(RemovableFileField, self).save_form_data(instance, data[0])
        if data and data[1]: # Delete file
            self.delete_file(instance)
            setattr(instance, self.name, None)

    def formfield(self, **kwargs):
        defaults = {'form_class': RemovableFileFormField}
        defaults.update(kwargs)
        return super(RemovableFileField, self).formfield(**defaults)


class RemovableImageField(models.ImageField, RemovableFileField):
    def formfield(self, **kwargs):
        defaults = {'form_class': RemovableImageFormField}
        defaults.update(kwargs)
        return super(RemovableFileField, self).formfield(**defaults)
