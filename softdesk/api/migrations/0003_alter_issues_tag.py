# Generated by Django 3.2.8 on 2022-01-28 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_issues_created_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issues',
            name='tag',
            field=models.CharField(choices=[('Bug', 'Incident'), ('Tâche', 'Ticket'), ('Amélioration', 'Change')], default='amélioration', max_length=20),
        ),
    ]
