# Generated by Django 5.1 on 2024-09-21 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_odds_id_in_match_alter_odds_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="match",
            name="bonds_available",
            field=models.IntegerField(default=40),
        ),
    ]
