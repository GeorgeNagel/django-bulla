from django.test import TestCase
from django.core.exceptions import ValidationError

from django_bulla.models.account import Account
from django_bulla.models.normals import Normals
from django_bulla.models.transaction_leg import TransactionLeg
from django_bulla.models.transaction import Transaction
from django_bulla.tests.factories.account import AccountFactory
from django_bulla.tests.factories.transaction_leg import TransactionLegFactory


class TestTransactionManager(TestCase):
    def test_credits_must_equal_debits(self):
        account_one = AccountFactory(normal=Normals.DEBIT)
        account_two = AccountFactory(normal=Normals.DEBIT)
        with self.assertRaisesRegex(ValidationError, "Debits must equal Credits"):
            debit = TransactionLegFactory.build(
                amount=1, normal=Normals.DEBIT, transaction=None
            )
            credit = TransactionLegFactory.build(
                amount=2, normal=Normals.CREDIT, transaction=None
            )
            Transaction.objects.create_from_transaction_legs(
                transaction_legs=[debit, credit]
            )

    def test_supports_more_than_two_legs(self):
        # In some situations, it can be useful to create
        # a Transaction with credits/debits in more than two accounts
        account_one = AccountFactory(normal=Normals.DEBIT)
        account_two = AccountFactory(normal=Normals.DEBIT)
        account_three = AccountFactory(normal=Normals.CREDIT)

        debit_one = TransactionLegFactory.build(
            account=account_one, normal=Normals.DEBIT, amount=1, transaction=None
        )
        debit_two = TransactionLegFactory.build(
            account=account_two, normal=Normals.DEBIT, amount=1, transaction=None
        )
        credit = TransactionLegFactory.build(
            account=account_three, normal=Normals.CREDIT, amount=2, transaction=None
        )
        Transaction.objects.create_from_transaction_legs(
            transaction_legs=[debit_one, debit_two, credit],
        )
        self.assertEqual(TransactionLeg.objects.count(), 3)

    def test_debit_journal_entries_increase_debit_normal_account_balance(self):
        account_one = AccountFactory(normal=Normals.DEBIT)
        account_two = AccountFactory(normal=Normals.DEBIT)
        self.assertEqual(account_one.balance, 0)

        # Debit a debit-normal account
        debit = TransactionLegFactory.build(
            amount=50, account=account_one, normal=Normals.DEBIT, transaction=None
        )
        credit = TransactionLegFactory.build(
            amount=50, account=account_two, normal=Normals.CREDIT, transaction=None
        )
        Transaction.objects.create_from_transaction_legs(
            transaction_legs=[debit, credit],
        )

        account_one.refresh_from_db()
        self.assertEqual(account_one.balance, 50)

    def test_debit_journal_entries_decrease_credit_normal_account_balance(self):
        account_one = AccountFactory(normal=Normals.CREDIT)
        account_two = AccountFactory(normal=Normals.CREDIT)
        self.assertEqual(account_one.balance, 0)

        # Debit a credit-normal account
        debit = TransactionLegFactory.build(
            amount=50, account=account_one, normal=Normals.DEBIT, transaction=None
        )
        credit = TransactionLegFactory.build(
            amount=50, account=account_two, normal=Normals.CREDIT, transaction=None
        )
        Transaction.objects.create_from_transaction_legs(
            transaction_legs=[debit, credit],
        )

        account_one.refresh_from_db()
        self.assertEqual(account_one.balance, -50)

    def test_credit_journal_entries_increase_credit_normal_account_balance(self):
        account_one = AccountFactory(normal=Normals.CREDIT)
        account_two = AccountFactory(normal=Normals.CREDIT)
        self.assertEqual(account_one.balance, 0)

        debit = TransactionLegFactory.build(
            amount=50, account=account_one, normal=Normals.DEBIT, transaction=None
        )
        # Credit a credit-normal account
        credit = TransactionLegFactory.build(
            amount=50, account=account_two, normal=Normals.CREDIT, transaction=None
        )
        Transaction.objects.create_from_transaction_legs(
            transaction_legs=[debit, credit],
        )

        account_two.refresh_from_db()
        self.assertEqual(account_two.balance, 50)

    def test_credit_journal_entries_decrease_debit_normal_account_balance(self):
        account_one = AccountFactory(normal=Normals.DEBIT)
        account_two = AccountFactory(normal=Normals.DEBIT)
        self.assertEqual(account_one.balance, 0)

        debit = TransactionLegFactory.build(
            amount=50, account=account_one, normal=Normals.DEBIT, transaction=None
        )
        # Credit a credit-normal account
        credit = TransactionLegFactory.build(
            amount=50, account=account_two, normal=Normals.CREDIT, transaction=None
        )
        Transaction.objects.create_from_transaction_legs(
            transaction_legs=[debit, credit],
        )

        account_two.refresh_from_db()
        self.assertEqual(account_two.balance, -50)
