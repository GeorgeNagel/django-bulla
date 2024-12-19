from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from django_bulla.models.statement import Statement
from django_bulla.models.normals import Normals
from django_bulla.models.transaction import Transaction
from django_bulla.models.transaction_leg import TransactionLeg
from django_bulla.tests.factories.account import AccountFactory


class TestStatement(TestCase):
    def test_save(self):
        account = AccountFactory(balance=0)
        statement = Statement.objects.create(
            account=account, balance=0, date_closed=timezone.now()
        )
        self.assertIsNotNone(statement.id)
        self.assertEqual(statement.balance, 0)
        self.assertIsNotNone(statement.date_closed)

    def test_cannot_save_invalid_balance(self):
        account = AccountFactory(balance=0)
        with self.assertRaisesRegexp(
            ValidationError,
            "Statement balance must equal sum of previous statement balance and all AccountEntries until date close",
        ):
            statement = Statement.objects.create(
                account=account, balance=123, date_closed=timezone.now()
            )

    def test_save_with_transactions(self):
        account_one = AccountFactory(balance=0, normal=Normals.DEBIT)
        account_two = AccountFactory(balance=0)
        debit = TransactionLeg(account=account_one, normal=Normals.DEBIT, amount=1)
        credit = TransactionLeg(account=account_two, normal=Normals.CREDIT, amount=1)
        Transaction.objects.create_from_transaction_legs(
            transaction_legs=[debit, credit]
        )
        account_one.refresh_from_db()
        self.assertEqual(account_one.balance, 1)

        try:
            statement = Statement.objects.create(
                account=account_one, balance=1, date_closed=timezone.now()
            )
        except ValidationError as e:
            self.fail(
                "Saving a Statement with the correct account balance should not raise an exception"
            )

    def test_statement_balance_must_match_sum_of_transactions(self):
        account_one = AccountFactory(balance=0, normal=Normals.DEBIT)
        account_two = AccountFactory(balance=0)
        debit = TransactionLeg(account=account_one, normal=Normals.DEBIT, amount=1)
        credit = TransactionLeg(account=account_two, normal=Normals.CREDIT, amount=1)
        Transaction.objects.create_from_transaction_legs(
            transaction_legs=[debit, credit]
        )
        # Manually set the account balance to an incorrect value
        account_one.balance = 123
        account_one.save()

        with self.assertRaisesRegexp(
            ValidationError,
            "Statement balance must equal sum of previous statement balance and all AccountEntries until date close",
        ):
            statement = Statement.objects.create(
                account=account_one, balance=123, date_closed=timezone.now()
            )
