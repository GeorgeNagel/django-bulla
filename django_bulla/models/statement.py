from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum, F
from django.db.models.functions import Now

from django_bulla.models.mixins import IdentifiableMixin
from django_bulla.models.transaction_leg import TransactionLeg


class StatementManager(models.Manager):
    def create(cls, *args, **kwargs):
        # Find the most recent statement before date_close, if any
        date_closed = kwargs.get("date_closed")
        account = kwargs.get("account")
        balance = kwargs.get("balance")
        previous_statement = (
            Statement.objects.filter(account=account, date_closed__lt=date_closed)
            .order_by("-date_closed")
            .first()
        )

        # Validate TransactionLegs since last Statement sum to expected balance
        transaction_legs_queryset = TransactionLeg.objects.filter(
            account=account,
            created__lt=date_closed,
        )
        if previous_statement:
            transaction_legs_queryset = transaction_legs_queryset.filter(
                created__gte=previous_statement.date_closed
            )
        transaction_legs_sum = (
            transaction_legs_queryset.aggregate(sum=Sum(F("amount") * F("normal")))[
                "sum"
            ]
            or 0
        )

        if previous_statement:
            expected_balance_on_date_closed = (
                previous_statement.balance + transaction_legs_sum
            )
        else:
            expected_balance_on_date_closed = transaction_legs_sum

        if expected_balance_on_date_closed != balance:
            raise ValidationError(
                "Statement balance must equal sum of previous statement balance and all AccountEntries until date close"
            )

        # Save Statement
        statement = Statement(**kwargs)
        statement.save()
        return statement


class Statement(IdentifiableMixin, models.Model):
    """
    Ties out the balance of an account on a particular date
    """

    # The account for which this statement was prepared
    account = models.ForeignKey("django_bulla.Account", on_delete=models.DO_NOTHING)

    # The date on which the balance of the Account was tied out
    date_closed = models.DateTimeField()

    # The balance of the Account on the close date
    balance = models.IntegerField()

    # Tracks when this record was inserted in the database
    # Note: when using Postgres, this should use
    # django.contrib.postgres.functions.TransactionNow instead
    # for consistent created timestamps within a db transaction
    created = models.DateTimeField(db_default=Now())

    objects = StatementManager()
