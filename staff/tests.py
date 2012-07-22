# Changing the staff member's first name, last name or email should change the user's as well
# Changing the staff member's first name or last name should change the slug
#   It would really be cool if you changed the slug, you check if redirects is
#   enabled and insert a redirect from the old slug to the new slug
# Changing the user's first name, last name or email should change the staff member's as well
# Changing the user's first name or last name should change the staff member's slug

from django.test import TestCase
from django.contrib.auth.models import User
from staff.models import StaffMember
from django.template.defaultfilters import slugify


class StaffTest(TestCase):
    """Tests for the Staff model"""
    def setUp(self):
        self.user = User.objects.create_user("tempuser", "tempuser", "temp@user.com")
        self.user.first_name = "Temporary"
        self.user.last_name = "User"
        self.user.save()

    def assertStaffInfoEqual(self, staffmember, user):
        self.assertEqual(staffmember.first_name, user.first_name)
        self.assertEqual(staffmember.last_name, user.last_name)
        self.assertEqual(staffmember.email, user.email)
        self.assertEqual(staffmember.slug, slugify('%s %s' % (user.first_name, user.last_name)))

    def testAutoCreation(self):
        self.assertEqual(StaffMember.objects.all().count(), 0)
        self.user.is_staff = True
        self.user.save()
        self.assertEqual(StaffMember.objects.all().count(), 1)
        s = self.user.staffmember_set.all()[0]
        self.assertStaffInfoEqual(s, self.user)

    def testAutoDeactivation(self):
        self.assertEqual(StaffMember.objects.all().count(), 0)
        self.user.is_staff = True
        self.user.save()
        self.assertEqual(StaffMember.objects.all().count(), 1)
        self.user.is_staff = False
        self.user.save()
        self.assertEqual(StaffMember.objects.all().count(), 1)
        self.assertEqual(StaffMember.objects.inactive().count(), 1)
        self.assertEqual(StaffMember.objects.active().count(), 0)
        s = self.user.staffmember_set.inactive()[0]
        self.assertEqual(s.is_active, False)

    def testUniqueSlug(self):
        self.user2 = User.objects.create_user("tempuser2", "tempuser", "temp@user.com")
        self.user2.first_name = "Temporary"
        self.user2.last_name = "User"
        self.user2.save()
        self.user.is_staff = True
        self.user.save()
        self.user2.is_staff = True
        self.user2.save()
        self.assertEquals(StaffMember.objects.all().count(), 2)
        slugs = StaffMember.objects.values_list('slug', flat=True)
        self.assertNotEqual(slugs[0], slugs[1])

    def testUserInfoChange(self):
        self.user.is_staff = True
        self.user.save()
        s = self.user.staffmember_set.all()[0]
        self.assertStaffInfoEqual(s, self.user)
        self.user.first_name = "Permanent"
        self.user.save()
        s = self.user.staffmember_set.all()[0]
        self.assertStaffInfoEqual(s, self.user)
