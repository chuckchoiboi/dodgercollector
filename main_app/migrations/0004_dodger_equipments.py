# Generated by Django 3.2 on 2021-04-21 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_auto_20210420_1913'),
    ]

    operations = [
        migrations.AddField(
            model_name='dodger',
            name='equipments',
            field=models.ManyToManyField(to='main_app.Equipment'),
        ),
    ]
