import factory

from django_bulla.models.transaction_leg import TransactionLeg
from django_bulla.models.normals import Normals
from test_app.tests.factories.account import AccountFactory
from test_app.tests.factories.transaction import TransactionFactory


class TransactionLegFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "django_bulla.TransactionLeg"

    amount = 0
    normal = Normals.DEBIT
    account = factory.SubFactory(AccountFactory)
    transaction = factory.SubFactory(TransactionFactory)
