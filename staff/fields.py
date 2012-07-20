from django import forms
from django.conf import settings
from django.db import models
from django.db.models.fields.files import ImageFieldFile
from django.utils.translation import ugettext as _
from django.core.files.images import get_image_dimensions

import os

URL_PREFIX = getattr(settings, 'STATIC_URL', settings.MEDIA_URL)


class DeleteCheckboxWidget(forms.CheckboxInput):
    """
    A specialzed checkbox that displays the filepath or preview and a
    checkbox to indicate that the file should be removed.
    """
    def __init__(self, *args, **kwargs):
        self.is_image = kwargs.pop('is_image')
        self.value = kwargs.pop('initial')
        super(DeleteCheckboxWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        value = value or self.value
        if value:
            html = u'<label for="%s">%s %s</label>' % (
                    attrs['id'],
                    super(DeleteCheckboxWidget, self).render(
                        name, False, attrs
                    ),
                    _('Delete')
                )
            if self.is_image:
                html += u'<br><img src="%s%s" width="50">' % (
                    URL_PREFIX, value
                )
            else:
                html += u'<br><a href="%s%s">%s</a>' % (
                    URL_PREFIX, value, os.path.basename(value)
                )
            return html
        else:
            return u''

    def _has_changed(self, initial, data):
        return data


class RemovableFileFormWidget(forms.MultiWidget):
    """
    A widget that shows the file input/upload widget and a delete checkbox
    for removing the file from the file storage
    """
    def __init__(self, is_image=False, initial=None, **kwargs):
        widgets = (forms.FileInput(), DeleteCheckboxWidget(
            is_image=is_image,
            initial=initial)
        )
        super(RemovableFileFormWidget, self).__init__(widgets)

    def decompress(self, value):
        return [None, value]


class RemovableFileFormField(forms.MultiValueField):
    """
    A field for forms that allows you to remove the file from the storage
    system within the admin
    """
    widget = RemovableFileFormWidget
    field = forms.FileField
    is_image = False

    def __init__(self, *args, **kwargs):
        fields = [
            self.field(*args, **kwargs),
            forms.BooleanField(required=False)
        ]
        # Compatibility with form_for_instance
        if kwargs.get('initial'):
            initial = kwargs['initial']
        else:
            initial = None
        self.widget = self.widget(is_image=self.is_image, initial=initial)
        super(RemovableFileFormField, self).__init__(
            fields, label=kwargs.pop('label'), required=False
        )

    def compress(self, data_list):
        return data_list


class RemovableImageFormField(RemovableFileFormField):
    """
    A specific form of image field that allows removal of the original file
    """
    field = forms.ImageField
    is_image = True


class RemovableFileField(models.FileField):
    """
    A field that allows you to remove the file from the storage system within
    the admin.
    """
    def delete_file(self, instance, sender, **kwargs):
        if getattr(instance, self.attname):
            image = getattr(instance, '%s' % self.name)
            file_name = image.path
            # If the file exists and no other object of this type references
            # it, delete it from the filesystem.
            instance_mgr = instance.__class__._default_manager
            filter_key = '%s__exact' % self.name
            filter_val = getattr(instance, self.attname)
            instance_pk = instance._get_pk_val()
            if os.path.exists(file_name) and not instance_mgr.filter(
                **{filter_key: filter_val}).exclude(pk=instance_pk):
                os.remove(file_name)

    def get_internal_type(self):
        return 'FileField'

    def save_form_data(self, instance, data):
        if data and data[0]:  # Replace file
            self.delete_file(instance, self)
            super(RemovableFileField, self).save_form_data(instance, data[0])
        if data and data[1]:  # Delete file
            self.delete_file(instance, self)
            setattr(instance, self.name, None)

    def formfield(self, **kwargs):
        defaults = {'form_class': RemovableFileFormField}
        defaults.update(kwargs)
        return super(RemovableFileField, self).formfield(**defaults)

    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        # We'll just introspect the _actual_ field.
        from south.modelsinspector import introspector
        field_class = "staff.fields.RemovableFileField"
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)


class MyImageFieldFile(ImageFieldFile):
    def _get_image_dimensions(self):
        if not hasattr(self, '_dimensions_cache'):
            try:
                close = self.closed
                self.open()
                self._dimensions_cache = get_image_dimensions(self, close=close)
            except IOError:
                self._dimensions_cache = (100, 100)
        return self._dimensions_cache


class RemovableImageField(models.ImageField, RemovableFileField):
    """
    A specific form of removeable file field, but specifically for images
    """
    attr_class = MyImageFieldFile

    def formfield(self, **kwargs):
        defaults = {'form_class': RemovableImageFormField}
        defaults.update(kwargs)
        return super(RemovableImageField, self).formfield(**defaults)
