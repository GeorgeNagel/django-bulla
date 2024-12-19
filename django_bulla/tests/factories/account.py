import factory

from django_bulla.models.account import Account
from django_bulla.models.normals import Normals


class AccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "django_bulla.Account"

    balance = 0
    normal = Normals.DEBIT
