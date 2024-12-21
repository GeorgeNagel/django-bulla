from django.apps import apps
from django.conf import settings
from django.contrib.postgres.functions import TransactionNow
from django.core.exceptions import ValidationError
from django.db import models, transaction as db_tx
from django.db.models import F
from django.db.models.functions import Now


from django_bulla.models.normals import Normals
from django_bulla.models.mixins import IdentifiableMixin


class TransactionManager(models.Manager):
    def create_from_transaction_legs(cls, *args, transaction_legs=None, **kwargs):
        """
        Create a Transaction from a list of unsaved TransactionLegs

        Args:
        transaction_legs: list - A list of unsaved TransactionLegs
        """
        if not isinstance(transaction_legs, list):
            raise ValidationError("Must provide a list of TransactionLegs")

        AccountModel = apps.get_model(settings.DJANGO_BULLA_ACCOUNT_MODEL)

        credits = 0
        debits = 0
        for transaction_leg in transaction_legs:
            if transaction_leg.normal == Normals.DEBIT:
                debits += transaction_leg.amount
            else:
                credits += transaction_leg.amount
        if credits != debits:
            raise ValidationError("Debits must equal Credits")

        account_ids = [
            transaction_leg.account_id for transaction_leg in transaction_legs
        ]
        TransactionModel = apps.get_model(settings.DJANGO_BULLA_TRANSACTION_MODEL)

        with db_tx.atomic():
            transaction = TransactionModel.objects.create(*args, **kwargs)
            AccountModel.objects.filter(id__in=account_ids).select_for_update()
            for transaction_leg in transaction_legs:
                # Save the TransactionLeg models
                transaction_leg.transaction = transaction
                transaction_leg.save()

                # We can optimize the number of round-trip queries to Postgres
                # by using atomic field updates if we don't care about potentially
                # creating debit balances on credit-normal accounts and vice-versa
                AccountModel.objects.filter(id=transaction_leg.account_id).update(
                    balance=F("balance")
                    + transaction_leg.amount * transaction_leg.normal * F("normal")
                )

        return transaction


class AbstractTransaction(IdentifiableMixin, models.Model):
    """
    A collection of Credits and Debits
    """

    objects = TransactionManager()

    # Tracks when this record was inserted in the database
    created = models.DateTimeField(db_default=TransactionNow())

    class Meta:
        abstract = True
