# Generated by Django 4.2.5 on 2024-09-08 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Channel",
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
                (
                    "deleted",
                    models.DateTimeField(db_index=True, editable=False, null=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "types",
                    models.CharField(
                        choices=[
                            ("marketplace", "Marketplace"),
                            ("shopify", "Shopify"),
                            ("pos", "POS"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        choices=[
                            ("shopee", "Shopee"),
                            ("tokopedia", "Tokopedia"),
                            ("blibli", "Blibli"),
                        ],
                        max_length=50,
                    ),
                ),
                ("slug", models.CharField(max_length=255, unique=True)),
                ("account_id", models.CharField(max_length=255)),
                ("account_name", models.CharField(max_length=255)),
                ("api_key", models.CharField(max_length=255)),
                ("api_secret", models.CharField(max_length=255)),
            ],
            options={
                "db_table": "app_channels_channels",
            },
        ),
        migrations.CreateModel(
            name="Store",
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
                (
                    "deleted",
                    models.DateTimeField(db_index=True, editable=False, null=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=100)),
                ("slug", models.SlugField(unique=True)),
                ("api_secret", models.CharField(max_length=100, unique=True)),
            ],
            options={
                "db_table": "app_channels_stores",
            },
        ),
        migrations.CreateModel(
            name="StockUpdate",
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
                (
                    "deleted",
                    models.DateTimeField(db_index=True, editable=False, null=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("product_id", models.UUIDField()),
                ("description", models.TextField()),
                ("stock", models.PositiveIntegerField(default=0)),
                (
                    "sync_status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("success", "Success"),
                            ("failed", "failed"),
                        ],
                        max_length=50,
                    ),
                ),
                ("last_sync_at", models.DateTimeField(blank=True, null=True)),
                ("err_message", models.CharField(max_length=255)),
                (
                    "channel",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="channel_stock_updates",
                        to="app_channels.channel",
                    ),
                ),
            ],
            options={
                "db_table": "app_channels_stock_updates",
            },
        ),
        migrations.CreateModel(
            name="OrderUpdate",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("order_id", models.CharField(max_length=125, unique=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("open", "open"),
                            ("pending", "Pending"),
                            ("processing", "Processing"),
                            ("shipped", "Shipped"),
                            ("delivered", "Delivered"),
                            ("canceled", "Canceled"),
                            ("refund", "Refund"),
                        ],
                        max_length=50,
                    ),
                ),
                ("message", models.CharField(max_length=255)),
                (
                    "channel",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="channel_order_updates",
                        to="app_channels.channel",
                    ),
                ),
            ],
            options={
                "db_table": "app_channels_order_updates",
            },
        ),
        migrations.AddField(
            model_name="channel",
            name="store",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="store_channels",
                to="app_channels.store",
            ),
        ),
    ]
