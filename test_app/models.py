from django.db import models

from django_bulla.models.account import AbstractAccount
from django_bulla.models.transaction import AbstractTransaction
from django_bulla.models.statement import AbstractStatement


class Account(AbstractAccount):
    pass


class Transaction(AbstractTransaction):
    pass


class Statement(AbstractStatement):
    pass
