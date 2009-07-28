from distutils.core import setup

setup(name='django-staff',
      version='0.1',
      description='A basic addition to auth.User that manages additional staff info',
      long_description='''In the Django Authentication package is that all users 
      use the same model/profile. This can be a drawback if you have lots of users 
      or you want different information stored for your staff members, such as bio, 
      contact info, etc. It is also handy for linking to models for author fields 
      so the lookup is quicker.
      
      The staff models are automatically created and managed by the 
      &quot;is_staff&quot; property of Users. Also, if you create a staff object, 
      it will set the &quot;is_staff&quot; object of the corresponding User object.''',
      author='Corey Oordt',
      author_email='coordt@washingtontimes.com',
      url='http://opensource.washingtontimes.com/projects/django-staff/',
      packages=['staff'],
      classifiers=['Development Status :: 4 - Beta',
          'Framework :: Django',
          ],
      )
