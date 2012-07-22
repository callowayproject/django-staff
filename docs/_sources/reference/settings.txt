========
Settings
========

.. contents::
   :depth:  1
   :local:
   :backlinks: top

Default Settings
================

.. code-block:: python

    DEFAULT_SETTINGS = {
        'PHOTO_STORAGE': settings.DEFAULT_FILE_STORAGE,
        'ORDERING': ('last_name', 'first_name'),
    }

.. _photo_storage_setting:

PHOTO_STORAGE
=============

**Default:** ``DEFAULT_FILE_STORAGE``

How you wish to store photos of staff members

.. _ordering_setting:

ORDERING
========

**Default:** ``('last_name', 'first_name')``

How the staff members are ordered in lists by default.