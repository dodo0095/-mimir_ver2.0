# Generated by Django 2.0 on 2019-08-21 14:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0003_pttdata_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pttdata',
            name='created',
        ),
        migrations.RemoveField(
            model_name='pttdata',
            name='last_modify_date',
        ),
    ]
