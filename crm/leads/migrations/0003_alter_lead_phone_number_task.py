# Generated by Django 5.0.1 on 2024-02-06 13:32

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0002_alter_lead_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='phone_number',
            field=models.CharField(max_length=12, unique=True, validators=[django.core.validators.RegexValidator(message="Номер телефона должен быть введен в формате: '+79999999999'", regex='^(\\+7)(\\d{10})$')]),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('task_date', models.DateField()),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='leads.lead')),
            ],
        ),
    ]
