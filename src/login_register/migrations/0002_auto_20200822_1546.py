# Generated by Django 3.1 on 2020-08-22 15:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login_register', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='dob',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='image',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='is_mobile_verified',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='mobile',
        ),
    ]
