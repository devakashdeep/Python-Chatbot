# Generated by Django 3.2.6 on 2021-08-12 16:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_intents'),
    ]

    operations = [
        migrations.RenameField(
            model_name='intents',
            old_name='customers',
            new_name='customer',
        ),
    ]
