# Generated by Django 5.1.4 on 2025-01-14 15:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Chatapp', '0002_rename_message_chatmessage_profile'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Profile',
        ),
    ]