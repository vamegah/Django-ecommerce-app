# Generated by Django 5.1.7 on 2025-03-27 20:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_userprofile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='address_1',
            new_name='address_line_1',
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='address_2',
            new_name='address_line_2',
        ),
    ]
