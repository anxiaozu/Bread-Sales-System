# Generated by Django 4.2.18 on 2025-02-10 06:43

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("bread_management", "0002_alter_bread_image"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="bread",
            options={
                "default_permissions": ("add", "change", "delete", "view"),
                "permissions": [("can_view_special_bread", "Can view special bread")],
            },
        ),
        migrations.AlterModelOptions(
            name="category",
            options={
                "default_permissions": ("add", "change", "delete", "view"),
                "permissions": [("can_manage_category", "Can manage category")],
            },
        ),
    ]
