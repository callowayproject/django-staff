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

def update_staff(sender, instance=None, **kwargs):
    """
    Modify or create staff upon User creation/editing
    """
    if not isinstance(instance, User):
        return
    
    try:
        member = StaffMember.objects.get(pk=instance.pk)
        if not instance.is_staff:
            member.is_active = False
            member.save()
    except StaffMember.DoesNotExist:
        if instance.is_staff:
            member = StaffMember(id=instance.pk,
                user=instance,
                first_name=instance.first_name,
                last_name=instance.last_name,
                slug=slugify('%s %s' % (instance.first_name, instance.last_name)),
                email=instance.email)
            
            try:
                member.save()
                member.sites.add(Site.objects.get(pk=settings.SITE_ID))
                member.save()
            except:
                return
    
post_save.connect(update_staff, sender=User) 