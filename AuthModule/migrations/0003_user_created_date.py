# Generated by Django 3.2.8 on 2021-10-22 12:51

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('AuthModule', '0002_remove_user_created_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='created_date',
            field=models.DateField(default=datetime.datetime(2021, 10, 22, 12, 51, 14, 41566, tzinfo=utc)),
        ),
    ]
