# Generated by Django 5.0.1 on 2024-04-15 17:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0013_task_date_of_creation_alter_task_task_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='deal',
            options={'ordering': ['-date_of_deal']},
        ),
        migrations.AlterField(
            model_name='lead',
            name='source',
            field=models.CharField(choices=[('Яндекс Директ', 'Яндекс Директ'), ('Вконтакте', 'Вконтакте'), ('Инстаграм', 'Инстаграм'), ('SEO', 'SEO'), ('Посоветовали', 'Посоветовали'), ('Прочее', 'Прочее')], max_length=20),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_date',
            field=models.DateField(default=datetime.date(2024, 4, 15)),
        ),
    ]
