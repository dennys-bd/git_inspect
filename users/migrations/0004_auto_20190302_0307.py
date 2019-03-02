# Generated by Django 2.1.7 on 2019-03-02 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20190302_0247'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(default='dennys-bd', max_length=255, unique=True),
            preserve_default=False,
        ),
    ]
