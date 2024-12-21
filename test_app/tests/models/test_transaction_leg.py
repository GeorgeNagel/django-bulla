from django.core.exceptions import ValidationError
from django.test import TestCase

from django_bulla.models.transaction_leg import TransactionLeg
from django_bulla.models.normals import Normals
from test_app.tests.factories.account import AccountFactory
from test_app.tests.factories.transaction import TransactionFactory


class TestTransactionLeg(TestCase):
    def test_save(self):
        transaction = TransactionFactory()
        account = AccountFactory()
        transaction_leg = TransactionLeg.objects.create(
            amount=1, normal=Normals.DEBIT, account=account, transaction=transaction
        )
        self.assertIsNotNone(transaction_leg.id)
        self.assertIsNotNone(transaction_leg.uuid)
        self.assertEqual(transaction_leg.amount, 1)
        self.assertEqual(transaction_leg.normal, Normals.DEBIT)
