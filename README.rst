============
Django Staff
============


In the Django Authentication package all users use the same model/profile. This can be a drawback if you have lots of users and you want different information stored for your staff members, such as bio, contact info, etc. It is also handy for linking to models for author fields so the lookup is quicker.

The staff models are automatically created and managed by the ``is_staff`` property of ``Users``. The staff profile is automatically added to the ``User`` admin screen.