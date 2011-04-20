from setuptools import setup, find_packages
import staff
import os

version = staff.get_version()

def read_file(filename):
    dirname = os.path.abspath(os.path.dirname(__file__))
    return open(os.path.join(dirname, filename)).read()

setup(name='django-staff',
      description='A basic addition to auth.User that manages additional staff info',
      long_description=read_file('README'),
      version=version,
      author='Corey Oordt',
      author_email='coordt@washingtontimes.com',
      url='http://github.com/washingtontimes/django-staff',
      include_package_files=True,
      packages=find_packages(),
      classifiers=['Framework :: Django',],
)
