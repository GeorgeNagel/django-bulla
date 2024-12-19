# Generated by Django 5.1.4 on 2024-12-19 16:39

import django.contrib.postgres.functions
import django.core.validators
import django.db.models.deletion
import django.db.models.functions.datetime
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('account_type', models.CharField(choices=[('system', 'System'), ('checking', 'Checking'), ('loans_receivable', 'Loans receivable'), ('credit_card', 'Credit card'), ('discount_allowed', 'Discount allowed')], default='Checking', max_length=16)),
                ('normal', models.IntegerField(choices=[(1, 'Debit'), (-1, 'Credit')])),
                ('balance', models.IntegerField(default=0)),
                ('created', models.DateTimeField(db_default=django.db.models.functions.datetime.Now())),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('created', models.DateTimeField(db_default=django.contrib.postgres.functions.TransactionNow())),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Statement',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('date_closed', models.DateTimeField()),
                ('balance', models.IntegerField()),
                ('created', models.DateTimeField(db_default=django.db.models.functions.datetime.Now())),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='django_bulla.account')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TransactionLeg',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('created', models.DateTimeField(db_default=django.db.models.functions.datetime.Now())),
                ('amount', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('normal', models.IntegerField(choices=[(1, 'Debit'), (-1, 'Credit')])),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='transaction_details', to='django_bulla.account')),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='details', to='django_bulla.transaction')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
