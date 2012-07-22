=======================
Customizing StaffMember
=======================

While the :py:class:`StaffMember` model is meant to be general, sometimes you need something extra. You can create your own subclass of :py:class:`StaffMember` for tweaking. In the example project you can browse the ``mystaff`` app. To test it out:

#. Comment out ``'staff',`` from ``INSTALLED_APPS`` in ``settings.py``
#. Uncomment ``'mystaff',`` from ``INSTALLED_APPS`` in ``settings.py``
#. Delete the ``dev.db`` file
#. Run ``./manage.py syncdb``
#. Create a new superuser when prompted


.. contents::
   :depth:  1
   :local:
   :backlinks: top

Create the custom class
=======================

Your custom :py:class:`StaffMember` model is going to subclass :py:class:`BaseStaffMember`, which is an abstract version of ``StaffMember``. Add your additional fields to the class.

.. literalinclude:: includes/mystaffmodel.py
    :linenos:
    :emphasize-lines: 7-8

Connect the signal
==================

You need to manually connect the ``post_save`` signal to a function that keeps your custom staff member class in sync.

.. literalinclude:: includes/mystaffmodel.py
    :linenos:
    :emphasize-lines: 2,5,11-12


#. Import :py:func:`get_staff_updater` from ``staff.models``. See line 5 in the example.
#. Execute it, passing in your model, and assign it to a variable. See line 11 in the example.
#. Import ``post_save`` from ``django.db.models.signals``. See line 2 in the example.
#. Finally connect the ``post_save`` signal to your staff updater variable as in line 12 in the example.

Create your admin class
=======================

The admin class is more complicated. It consists of three parts: customizing the :py:class:`StaffMemberAdmin` class, creating a custom :py:class:`UserAdmin`, and finally swapping out the currently registered ``UserAdmin`` class with yours.

Your own admin class
--------------------

Your admin class simply needs to redefine the fieldsets and model of the :py:class:`StaffMemberAdmin` class.

.. literalinclude:: includes/mystaffadmin.py
    :linenos:
    :emphasize-lines: 4,6,9-15

The class is very straightforward. Since we only added one field, ``github``, we copy the ``fieldsets`` value from the base class and add that field in.

Then we set the model to our new model.

Making a custom User admin class
--------------------------------

We need to add an inline class to the current :py:class:`UserAdmin`.

.. literalinclude:: includes/mystaffadmin.py
    :linenos:
    :emphasize-lines: 2,17-21

This is merely sublassing the existing :py:class:`UserAdmin` and adding our own ``inlines`` attribute equal to a list containing the new admin class defined above.

Re-registering the UserAdmin
----------------------------

Now we carefully swap the old ``UserAdmin`` with our ``UserAdmin`` subclass.

.. literalinclude:: includes/mystaffadmin.py
    :linenos:
    :emphasize-lines: 1,3,23-24

Django's admin has the ability to both register an admin class and unregister an admin class. After removing any admin classes associated with the :py:class:`User` class, we register and associate our custom user admin class.

Gather the templates
====================

Django staff includes a set of templates for various Django versions. Since we'll remove ``'staff'`` from ``INSTALLED_APPS``, Django won't find them any more. We need to copy them into either the project's templates directory or your application's template directory.

The templates, named ``staff.html`` and ``staff13.html``, need to go into::

    templates
       admin
          edit_inline
             staff.html
             staff13.html

Remove staff from INSTALLED_APPS
================================

If Django Staff is still included in your ``INSTALLED_APPS`` setting, you'll have a bit of redundancy. Make sure that ``'staff'`` is not in that list. It still must remain available to your new application, so don't don't uninstall the library.