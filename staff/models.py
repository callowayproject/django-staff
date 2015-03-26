from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_localflavor_us.models import PhoneNumberField
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.template.defaultfilters import slugify
from django.core.files.storage import get_storage_class

from fields import RemovableImageField
from .settings import PHOTO_STORAGE, ORDERING

DEFAULT_STORAGE = get_storage_class(PHOTO_STORAGE)


class StaffMemberManager(models.Manager):
    """
    A Manager for StaffMembers.
    """
    def active(self):
        """
        Return only the current staff members
        """
        qset = super(StaffMemberManager, self).get_query_set()
        return qset.filter(is_active=True)

    def inactive(self):
        """
        Return inactive staff members
        """
        qset = super(StaffMemberManager, self).get_query_set()
        return qset.filter(is_active=False)


class BaseStaffMember(models.Model):
    """
    A User that works for the organization.
    """
    user = models.ForeignKey(User,
        limit_choices_to={'is_active': True},
        unique=True, verbose_name=_('User'))
    first_name = models.CharField(_('First Name'),
        max_length=150,
        help_text=_("""This field is linked to the User account and will
                    change its value."""),
        blank=True,
        null=True)
    last_name = models.CharField(_('Last Name'),
        max_length=150,
        help_text=_("""This field is linked to the User account and will
                    change its value."""),
        blank=True,
        null=True)
    slug = models.SlugField(unique=True)
    email = models.EmailField(_('e-mail'),
        blank=True,
        help_text=_("""This field is linked to the User account and will
                    change its value."""),
        null=True)
    bio = models.TextField(_('Biography'), blank=True)
    is_active = models.BooleanField(_('is a current employee'), default=True)
    phone = PhoneNumberField(_('Phone Number'), blank=True)
    photo = RemovableImageField(_('Photo'),
        blank=True,
        upload_to='img/staff/%Y',
        storage=DEFAULT_STORAGE(),
        height_field='photo_height',
        width_field='photo_width')
    photo_height = models.IntegerField(default=0, blank=True)
    photo_width = models.IntegerField(default=0, blank=True)
    twitter = models.CharField(_('Twitter ID'),
        max_length=100,
        blank=True)
    facebook = models.CharField(_('Facebook Acccount'),
        max_length=100,
        blank=True)
    google_plus = models.CharField(_('Google+ ID'),
        max_length=100,
        blank=True)
    website = models.URLField(_('Website'),
        blank=True)
    sites = models.ManyToManyField(Site)

    objects = StaffMemberManager()

    class Meta:
        ordering = ORDERING
        abstract = True

    def __unicode__(self):
        return u"%s %s" % (self.first_name, self.last_name)

    @models.permalink
    def get_absolute_url(self):
        """
        The URL
        """
        return ('staff_staffmember_detail', [self.slug])

    def get_full_name(self):
        """
        Simple method to concatenate the name
        """
        return u'%s %s' % (self.first_name.strip(), self.last_name.strip())

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        """
        Makes sure we are in sync with the User field
        """
        self.first_name = self.user.first_name
        self.last_name = self.user.last_name
        self.email = self.user.email
        full_name = '%s %s' % (self.first_name, self.last_name)
        theslug = slugify(full_name)
        if not theslug.strip():
            theslug = str(self.user.pk)
        while self.__class__.objects.filter(slug=theslug).exclude(pk=self.pk).count():
            theslug = "%s_" % theslug
        if self.slug != theslug:
            self.slug = theslug
        self.slug = self.slug[:50]
        super(BaseStaffMember, self).save(
            force_insert, force_update, *args, **kwargs
        )


class StaffMember(BaseStaffMember):
    pass


def get_staff_updater(cls):
    """
    This returns a function for passing to a signal.
    """
    from django.core.exceptions import ImproperlyConfigured
    if not issubclass(cls, BaseStaffMember):
        raise ImproperlyConfigured("%s is not a sublass of StaffMember" % cls)

    def update_staff_member(sender, instance, created, *args, **kwargs):
        """
        Update the Staff Member instance when a User object is changed.
        """
        if instance.is_staff and not cls.objects.filter(user=instance).count():
            staffmember = cls(
                user=instance,
                is_active=True)
            staffmember.save()
            for site in Site.objects.all():
                staffmember.sites.add(site)
        elif instance.is_staff:
            staffmembers = cls.objects.filter(user=instance)
            if len(staffmembers):
                staffmember = staffmembers[0]
                staffmember.is_active = True
                if instance.first_name != staffmember.first_name:
                    staffmember.first_name = instance.first_name
                    staffmember.slug = slugify('%s %s' % (
                        instance.first_name, instance.last_name))
                if instance.last_name != staffmember.last_name:
                    staffmember.last_name = instance.last_name
                    staffmember.slug = slugify('%s %s' % (
                        instance.first_name, instance.last_name))
                if instance.email != staffmember.email:
                    staffmember.email = instance.email
                staffmember.save()
        elif not instance.is_staff:
            # Make sure we deactivate any staff members associated with this user
            for staffmember in cls.objects.filter(user=instance):
                staffmember.is_active = False
                staffmember.save()
        from django.db import transaction
        transaction.commit_unless_managed()

    return update_staff_member

from django.conf import settings

if 'staff' in settings.INSTALLED_APPS:
    from django.db.models.signals import post_save
    update_staff_member = get_staff_updater(StaffMember)
    post_save.connect(update_staff_member, sender=User)
