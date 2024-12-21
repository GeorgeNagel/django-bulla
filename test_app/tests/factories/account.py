import factory

from test_app.models import Account
from django_bulla.models.normals import Normals


class AccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "test_app.Account"

    balance = 0
    normal = Normals.DEBIT
