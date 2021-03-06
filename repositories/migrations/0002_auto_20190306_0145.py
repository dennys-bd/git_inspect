# Generated by Django 2.1.7 on 2019-03-06 01:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('repositories', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='repository',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='commit',
            name='repository',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repositories.Repository'),
        ),
        migrations.AlterUniqueTogether(
            name='repository',
            unique_together={('name', 'user')},
        ),
    ]
