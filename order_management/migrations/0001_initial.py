# Generated by Django 4.2.17 on 2025-01-13 13:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("bread_management", "0001_initial"),
        ("user_management", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.IntegerField()),
                ("order_date", models.DateTimeField(auto_now_add=True)),
                ("total_price", models.DecimalField(decimal_places=2, max_digits=7)),
                (
                    "bread",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bread_management.bread",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="user_management.user",
                    ),
                ),
            ],
        ),
    ]
