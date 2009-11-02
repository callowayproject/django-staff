#TODO setup signal to automatically add a staff user
# when a django.contrib.auth.models.User is created
# with is_staff=True, and also deactivate a staff
# member when is_staff is set to False
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.contrib.sites.models import Site
from staff.models import StaffMember
