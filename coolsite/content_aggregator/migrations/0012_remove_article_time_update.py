# Generated by Django 4.0.3 on 2022-05-31 05:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content_aggregator', '0011_article_views'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='time_update',
        ),
    ]
