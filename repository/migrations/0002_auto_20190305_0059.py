# Generated by Django 2.1.7 on 2019-03-05 00:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commit',
            name='commiter',
        ),
        migrations.AddField(
            model_name='commit',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='commit',
            name='message',
            field=models.TextField(blank=True),
        ),
    ]