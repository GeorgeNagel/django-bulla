from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.functions import Now

from django_bulla.models.mixins import IdentifiableMixin


class TransactionLeg(IdentifiableMixin, models.Model):
    """
    Represents a single Debit or Credit of a Transaction
    """

    class Normals(models.IntegerChoices):
        DEBIT = 1
        CREDIT = -1

    # The Transaction to which this debit/credit belongs
    transaction = models.ForeignKey(
        "django_bulla.Transaction",
        on_delete=models.DO_NOTHING,
        related_name="details",
    )

    # Account to which the debit/credit relates
    account = models.ForeignKey(
        "django_bulla.Account",
        on_delete=models.DO_NOTHING,
        related_name="transaction_details",
    )

    # Tracks when this record was inserted in the database
    # Note: when using Postgres, this should use
    # django.contrib.postgres.functions.TransactionNow instead
    # for consistent created timestamps within a db transaction
    created = models.DateTimeField(db_default=Now())

    # The value of the debit/credit.
    # Amounts should always be positive.
    # Values are in cents.
    amount = models.IntegerField(validators=[MinValueValidator(1)])

    # Normal factor represents whether this is a debit (+1 normal)
    # or credit (-1 normal)
    normal = models.IntegerField(choices=Normals)
