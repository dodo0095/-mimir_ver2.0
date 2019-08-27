# Generated by Django 2.0 on 2019-08-21 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='pttdata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('author', models.TextField()),
                ('title', models.TextField()),
                ('href', models.TextField()),
                ('pushcount', models.IntegerField()),
                ('last_modify_date', models.DateTimeField()),
                ('created', models.DateTimeField()),
            ],
            options={
                'db_table': 'pttdata',
            },
        ),
    ]
