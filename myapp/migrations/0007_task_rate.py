# Generated by Django 3.2.16 on 2022-10-29 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_auto_20221029_0024'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='rate',
            field=models.CharField(choices=[(20, 20), (40, 40), (60, 60), (80, 80), (100, 100)], default=20, max_length=100),
        ),
    ]
