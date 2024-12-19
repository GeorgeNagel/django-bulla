from django.test import TestCase

from django_bulla.models.account import Account
from django_bulla.models.normals import Normals


class TestAccount(TestCase):
    def test_save(self):
        account = Account.objects.create(normal=Normals.DEBIT)
        self.assertIsNotNone(account.id)
        self.assertEqual(account.balance, 0)
        self.assertEqual(account.normal, Normals.DEBIT)
