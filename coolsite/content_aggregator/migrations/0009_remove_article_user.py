# Generated by Django 4.0.3 on 2022-05-19 15:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content_aggregator', '0008_alter_userprofile_user_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='user',
        ),
    ]