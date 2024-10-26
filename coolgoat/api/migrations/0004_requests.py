# Generated by Django 5.1 on 2024-09-28 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_match_bonds_available'),
    ]

    operations = [
        migrations.CreateModel(
            name='Requests',
            fields=[
                ('request_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('group_id', models.CharField(max_length=255)),
                ('fixture_id', models.IntegerField()),
                ('league_name', models.CharField(max_length=255)),
                ('round', models.CharField(max_length=255)),
                ('date', models.DateTimeField()),
                ('result', models.CharField(max_length=255)),
                ('deposit_token', models.CharField(max_length=255)),
                ('datetime', models.CharField(max_length=255)),
                ('quantity', models.IntegerField()),
                ('seller', models.IntegerField()),
                ('validated', models.BooleanField(default=False)),
            ],
        ),
    ]