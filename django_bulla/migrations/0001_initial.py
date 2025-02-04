# Generated by Django 5.1.4 on 2024-12-21 21:25

from django.conf import settings
import django.core.validators
import django.db.models.deletion
import django.db.models.functions.datetime
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("test_app", "__first__"),
    ]

    operations = [
        migrations.CreateModel(
            name="TransactionLeg",
            fields=[
                (
                    "id",
                    models.AutoField(primary_key=True, serialize=False, unique=True),
                ),
                ("uuid", models.UUIDField(default=uuid.uuid4, unique=True)),
                (
                    "created",
                    models.DateTimeField(
                        db_default=django.db.models.functions.datetime.Now()
                    ),
                ),
                (
                    "amount",
                    models.IntegerField(
                        validators=[django.core.validators.MinValueValidator(1)]
                    ),
                ),
                ("normal", models.IntegerField(choices=[(1, "Debit"), (-1, "Credit")])),
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="transaction_details",
                        to=settings.DJANGO_BULLA_ACCOUNT_MODEL,
                    ),
                ),
                (
                    "transaction",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="details",
                        to=ettings.DJANGO_BULLA_TRANSACTION_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
