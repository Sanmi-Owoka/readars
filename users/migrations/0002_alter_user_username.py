# Generated by Django 4.1.7 on 2023-03-29 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
    ]
