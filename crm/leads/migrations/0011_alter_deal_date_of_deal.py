# Generated by Django 5.0.1 on 2024-03-01 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0010_deal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deal',
            name='date_of_deal',
            field=models.DateField(auto_now_add=True),
        ),
    ]
