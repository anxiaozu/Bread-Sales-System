# Generated by Django 4.2.18 on 2025-02-13 11:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bread_management", "0005_category_breads"),
    ]

    operations = [
        migrations.AddField(
            model_name="bread",
            name="hardness",
            field=models.CharField(
                choices=[
                    ("soft", "软乎"),
                    ("moderate", "适中"),
                    ("hardish", "偏硬"),
                    ("hard", "硬"),
                ],
                default="moderate",
                max_length=10,
            ),
        ),
        migrations.AddField(
            model_name="bread",
            name="sugar_content",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
    ]
