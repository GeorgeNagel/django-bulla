from django.utils import timezone
import factory

from test_app.tests.factories.account import AccountFactory


class StatementFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "test_app.Statement"

    balance = 0
    account = factory.SubFactory(AccountFactory)
    date_closed = factory.lazy_attribute(lambda obj: timezone.now())
