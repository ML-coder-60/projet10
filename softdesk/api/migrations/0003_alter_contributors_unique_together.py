# Generated by Django 3.2.8 on 2022-01-06 18:04

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0002_alter_contributors_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='contributors',
            unique_together={('contributor', 'project')},
        ),
    ]