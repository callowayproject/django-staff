from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from staff.models import BaseStaffMember, get_staff_updater

class MyStaffMember(BaseStaffMember):
    github = models.CharField(max_length=50, blank=True)


update_staff_member = get_staff_updater(MyStaffMember)
post_save.connect(update_staff_member, sender=User)