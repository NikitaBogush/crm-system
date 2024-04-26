# Generated by Django 5.0.1 on 2024-04-26 06:19

import django.utils.timezone
import leads.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0018_lead_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deal',
            name='date_of_deal',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='lead',
            name='date_of_creation',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='lead',
            name='phone_number',
            field=models.CharField(max_length=12, unique=True, validators=[leads.validators.phone_regex]),
        ),
    ]