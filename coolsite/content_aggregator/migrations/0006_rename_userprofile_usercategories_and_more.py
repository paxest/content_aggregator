# Generated by Django 4.0.3 on 2022-05-13 11:11

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('content_aggregator', '0005_userprofile_delete_usercategory'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserProfile',
            new_name='UserCategories',
        ),
        migrations.AlterModelOptions(
            name='usercategories',
            options={'verbose_name': 'Категории пользователя', 'verbose_name_plural': 'Категории пользователя'},
        ),
    ]
