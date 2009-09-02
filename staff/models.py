from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _
from django.contrib.localflavor.us.models import PhoneNumberField
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.template.defaultfilters import slugify


class StaffMemberManager(models.Manager):
    """
    A Manager for StaffMembers.
    """
    def active(self):
        return super(StaffMemberManager, self).get_query_set().filter(is_active=True)


class StaffMember(models.Model):
    user = models.ForeignKey(User, limit_choices_to = {'is_staff': False, 'is_active'=True})
    first_name = models.CharField(_('First Name'),
        max_length=150,
        help_text=_('This field is linked to the User account and will change its value.'))
    last_name = models.CharField(_('Last Name'),
        max_length=150,
        help_text=_('This field is linked to the User account and will change its value.'))
    slug = models.SlugField(unique=True)
    email = models.EmailField(_('e-mail'), 
        blank=True,
        help_text=_('This field is linked to the User account and will change its value.'))
    bio = models.TextField(_('Biography'), blank=True)
    is_active = models.BooleanField(_('is a current employee'), default=True)
    phone = PhoneNumberField(_('Phone Number'), blank=True)
    photo = models.FileField(_('Photo'), blank=True, upload_to='img/staff/%Y')
    sites = models.ManyToManyField(Site)
    
    objects = StaffMemberManager()
    
    class Meta:
        ordering = ('last_name', 'first_name')

    def __unicode__(self):
        return u"%s %s" % (self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('staff_staffmember_detail', args=[self.slug])

    def get_full_name(self):
        return u'%s %s' % (self.first_name.strip(), self.last_name.strip())
    
    def save(self, *args, **kwargs):
        """
        Makes sure the User field is in sync with the values here
        """
        theslug = slugify('%s %s' % (self.first_name, self.last_name))
        while StaffMember.objects.filter(slug=theslug).count():
            theslug = "%s_" % theslug
        if self.slug != theslug:
            self.slug = theslug
        super(StaffMember, self).save(*args, **kwargs)
        must_save_user = False
        if self.first_name != self.user.first_name:
            self.user.first_name = self.first_name
            must_save_user = True
        if self.last_name != self.user.last_name:
            self.user.last_name = self.last_name
            must_save_user = True
        if self.email != self.user.email:
            self.user.email = self.email
            must_save_user = True
        if must_save_user:
            self.user.is_staff = True
            self.user.save()

def update_staff_member(sender, instance, created, **kwargs):
    """
    Update the Staff Member instance when a User object is changed.
    """
    if created and instance.is_staff and not instance.staffmember_set.count():
        staffmember,_ = instance.staffmember_set.get_or_create(
            first_name=instance.first_name, 
            last_name=instance.last_name,
            slug=slugify('%s %s' % (instance.first_name, instance.last_name)),
            email=instance.email,
            is_active=True)
        for site in Site.objects.all():
            staffmember.sites.add(site)
    elif instance.is_staff:
        must_save = False
        staffmembers = instance.staffmember_set.all()
        if len(staffmembers):
            staffmember = staffmembers[0]
            if instance.first_name != staffmember.first_name:
                staffmember.first_name = instance.first_name
                staffmember.slug = slugify('%s %s' % (instance.first_name, instance.last_name)),
                must_save = True
            if instance.last_name != staffmember.last_name:
                staffmember.last_name = instance.last_name
                staffmember.slug = slugify('%s %s' % (instance.first_name, instance.last_name)),
                must_save = True
            if instance.email != staffmember.email:
                staffmember.email = instance.email
                must_save = True
            if must_save:
                staffmember.save()
    elif not instance.is_staff:
        # Make sure we deactiviate any staff members associated with this user
        for staffmember in instance.staffmember_set.all():
            staffmember.is_active = False
            staffmemeber.save()

from django.db.models.signals import post_save
post_save.connect(update_staff_member, sender=User)