# Generated by Django 2.1.7 on 2019-03-06 01:45

import datetime
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Commit',
            fields=[
                ('sha', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('url', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('author', django.contrib.postgres.fields.jsonb.JSONField()),
                ('message', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('github_id', models.IntegerField(unique=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255, null=True)),
                ('url', models.CharField(max_length=255)),
            ],
        ),
    ]