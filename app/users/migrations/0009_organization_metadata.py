# Generated by Django 4.0 on 2021-12-24 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_driver_type_delete_drivertype'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='metadata',
            field=models.JSONField(default=dict),
        ),
    ]
