# Generated by Django 5.1 on 2024-09-30 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CoolgoatUser',
            fields=[
                ('email', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('funds', models.IntegerField()),
            ],
        ),
    ]
