from django.utils import timezone
import factory

from django_bulla.models.normals import Normals
from test_app.models import Transaction


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "test_app.Transaction"


class TransactionWithDebitAndCredit(factory.django.DjangoModelFactory):
    amount = 1
    created = factory.lazy_attribute(lambda obj: timezone.now())
    debit = factory.RelatedFactory(
        "test_app.tests.factories.transaction_leg.TransactionLegFactory",
        factory_related_name="transaction",
        normal=Normals.DEBIT,
        amount=factory.SelfAttribute("..amount"),
        created=factory.SelfAttribute("..created"),
    )
    credit = factory.RelatedFactory(
        "test_app.tests.factories.transaction_leg.TransactionLegFactory",
        factory_related_name="transaction",
        normal=Normals.CREDIT,
        amount=factory.SelfAttribute("..amount"),
        created=factory.SelfAttribute("..created"),
    )

    class Meta:
        model = "test_app.Transaction"
        exclude = ("debit", "credit", "amount", "created")
