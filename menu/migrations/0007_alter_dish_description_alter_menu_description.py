# Generated by Django 5.0.3 on 2024-03-25 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("menu", "0006_alter_menu_added_on_alter_menu_updated_on"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dish",
            name="description",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="menu",
            name="description",
            field=models.TextField(blank=True),
        ),
    ]
