# Generated by Django 3.2.6 on 2021-12-14 14:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0002_rename_follower_connection_conn_follower'),
    ]

    operations = [
        migrations.RenameField(
            model_name='connection',
            old_name='conn_follower',
            new_name='follower',
        ),
    ]