import os
from setuptools import setup, find_packages


def read_file(filename):
    """Read a file into a string"""
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        return open(filepath).read()
    except IOError:
        return ''


def get_readme():
    """Return the README file contents. Supports text,rst, and markdown"""
    for name in ('README', 'README.rst', 'README.md'):
        if os.path.exists(name):
            return read_file(name)
    return ''

# Use the docstring of the __init__ file to be the description
DESC = " ".join(__import__('staff').__doc__.splitlines()).strip()

setup(name='django-staff',
      description=DESC,
      long_description=get_readme(),
      version=__import__('staff').get_version().replace(' ', '-'),
      author='Corey Oordt',
      author_email='webmaster@callowayproject.com',
      url='https://github.com/callowayproject/django-staff',
      include_package_data=True,
      install_requires=read_file('requirements.txt'),
      packages=find_packages(),
      classifiers=['Framework :: Django'],
)
