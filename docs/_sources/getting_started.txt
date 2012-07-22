===============
Getting Started
===============

.. contents::
   :depth:  1
   :local:
   :backlinks: top

Installation
============

#. ``pip install django-staff``

#. Add to ``INSTALLED_APPS`` in ``settings.py``

How it works
============

#. Django Staff modifies (monkey patches) Django's built-in :py:class:`User` model's admin, adding an inline form to the :py:class:`Staff` model.

#. Django Staff registers a listener to updates to the :py:class:`User` model.

#. Three possible actions can happen when a :py:class:`User` is created or changed:

    #. A staff object is created, linked to the user object and permission is added for all available sites.

    #. The existing staff object is updated, keeping the first name, last name and e-mail in sync and also confirming the active status of the staff object.

    #. The existing staff object is marked as inactive

Using Django Staff
==================

#. Create a new :py:class:`User`

#. Make sure their ``staff status`` is checked

#. Click the ``Save and continue editing`` button.

#. When the page reloads, you'll notice the additional fields at the bottom of the page.