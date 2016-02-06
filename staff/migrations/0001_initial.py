# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.files.storage
from django.conf import settings
import django_localflavor_us.models
import staff.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='StaffMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(help_text='This field is linked to the User account and will\n                    change its value.', max_length=150, null=True, verbose_name='First Name', blank=True)),
                ('last_name', models.CharField(help_text='This field is linked to the User account and will\n                    change its value.', max_length=150, null=True, verbose_name='Last Name', blank=True)),
                ('slug', models.SlugField(unique=True)),
                ('email', models.EmailField(help_text='This field is linked to the User account and will\n                    change its value.', max_length=75, null=True, verbose_name='e-mail', blank=True)),
                ('bio', models.TextField(verbose_name='Biography', blank=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='is a current employee')),
                ('phone', django_localflavor_us.models.PhoneNumberField(max_length=20, verbose_name='Phone Number', blank=True)),
                ('photo', staff.fields.RemovableImageField(upload_to=b'img/staff/%Y', width_field=b'photo_width', storage=django.core.files.storage.FileSystemStorage(), height_field=b'photo_height', blank=True, verbose_name='Photo')),
                ('photo_height', models.IntegerField(default=0, blank=True)),
                ('photo_width', models.IntegerField(default=0, blank=True)),
                ('twitter', models.CharField(max_length=100, verbose_name='Twitter ID', blank=True)),
                ('facebook', models.CharField(max_length=100, verbose_name='Facebook Acccount', blank=True)),
                ('google_plus', models.CharField(max_length=100, verbose_name='Google+ ID', blank=True)),
                ('website', models.URLField(verbose_name='Website', blank=True)),
                ('sites', models.ManyToManyField(to='sites.Site')),
                ('user', models.ForeignKey(verbose_name='User', to=settings.AUTH_USER_MODEL, unique=True)),
            ],
            options={
                'ordering': ('last_name', 'first_name'),
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
