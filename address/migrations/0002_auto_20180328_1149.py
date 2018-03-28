# Generated by Django 2.0.2 on 2018-03-28 03:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contactinfo',
            name='person',
        ),
        migrations.AddField(
            model_name='personalinfo',
            name='contact_number',
            field=models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')]),
        ),
        migrations.DeleteModel(
            name='ContactInfo',
        ),
    ]