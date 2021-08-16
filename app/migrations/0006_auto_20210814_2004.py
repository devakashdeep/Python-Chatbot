# Generated by Django 3.2.6 on 2021-08-14 14:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0005_customers_last_login'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customers',
            name='email',
        ),
        migrations.RemoveField(
            model_name='customers',
            name='last_login',
        ),
        migrations.RemoveField(
            model_name='customers',
            name='name',
        ),
        migrations.RemoveField(
            model_name='customers',
            name='password',
        ),
        migrations.RemoveField(
            model_name='customers',
            name='username',
        ),
        migrations.AddField(
            model_name='customers',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
