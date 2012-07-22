from django.conf import settings

DEFAULT_SETTINGS = {
    'PHOTO_STORAGE': settings.DEFAULT_FILE_STORAGE,
    'ORDERING': ('last_name', 'first_name'),
}

USER_SETTINGS = DEFAULT_SETTINGS.copy()

if hasattr(settings, 'STAFF_ORDERING'):
    USER_SETTINGS['ORDERING'] = settings.STAFF_ORDERING

if hasattr(settings, 'STAFF_PHOTO_STORAGE'):
    USER_SETTINGS['PHOTO_STORAGE'] = settings.STAFF_PHOTO_STORAGE

globals().update(USER_SETTINGS)