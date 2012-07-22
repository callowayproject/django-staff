=====================
Staff Model Reference
=====================

StaffMember
===========

.. py:class:: StaffMember

   .. py:attribute:: user

      **Required** :py:class:`ForeignKey` :py:class:`User`

      The :py:class:`User` to which this profile relates. Choices are limited to active users.

   .. py:attribute:: first_name

      ``CharField(150)``

      The first name of the user. It is automatically synced with the user object and is provided in this model for convenience.

   .. py:attribute:: last_name

      ``CharField(150)``

      The last name of the user. It is automatically synced with the user object and is provided in this model for convenience.

   .. py:attribute:: slug

      **Required** ``SlugField``

      A URL-friendly version of the first and last name.

   .. py:attribute:: email

      ``EmailField``

      The email address of the user. It is automatically synced with the user object and is provided in this model for convenience.

   .. py:attribute:: bio

      ``TextField``

      An in-depth, riveting account of the user's life.

   .. py:attribute:: is_active

      **Required** ``BooleanField`` *Default:* ``True``

      ``True`` indicates a current staff member. ``False`` indicates a former staff member.

   .. py:attribute:: phone

      ``PhoneNumberField``

      A series of digits which, when typed into telephonic devices, might establish a vocal connection to the user.

   .. py:attribute:: photo

      ``RemovableImageField``

      A visual, digital representation of the user. The image is stored based on the :ref:`photo_storage_setting` setting.

   .. py:attribute:: photo_height

      ``IntegerField``

      An automatically-managed reference to the height of the uploaded photo.

   .. py:attribute:: photo_width

      ``IntegerField``

      An automatically-managed reference to the width of the uploaded photo.

   .. py:attribute:: twitter

      ``CharField(100)``

      The staff member's Twitter ID

   .. py:attribute:: facebook

      ``CharField(100)``

      The staff member's Facebook ID

   .. py:attribute:: google_plus

      ``CharField(100)``

      The staff member's Google Plus account

   .. py:attribute:: website

      ``URLField``

      A custom web site for the staff member.

   .. py:attribute:: sites

      ``ManyToManyField`` :py:class:`Site`

      The sites that the staff member works on.

   .. py:method:: get_full_name

      A convenient way to concatenate the first and last name.

      :returns: `unicode`
