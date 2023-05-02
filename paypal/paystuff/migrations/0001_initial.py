# Generated by Django 4.1.7 on 2023-04-28 14:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BillingAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('addressLine1', models.CharField(max_length=30)),
                ('addressLine2', models.CharField(max_length=30)),
                ('city', models.CharField(max_length=20)),
                ('postcode', models.CharField(max_length=10)),
                ('region', models.CharField(max_length=20)),
                ('countryCode', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='CardDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.BigIntegerField()),
                ('cvv', models.SmallIntegerField()),
                ('expiryDate', models.CharField(max_length=5)),
                ('billingAddress', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='paystuff.billingaddress')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('transaction_id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('orderId', models.CharField(max_length=30)),
                ('userId', models.CharField(max_length=30)),
                ('merchantId', models.CharField(max_length=30)),
                ('currencyCode', models.CharField(max_length=30)),
                ('transactionAmount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('deliveryEmail', models.CharField(max_length=30)),
                ('deliveryName', models.CharField(max_length=30)),
                ('dateCreated', models.DateField(auto_now_add=True)),
                ('status', models.CharField(choices=[('new', 'New'), ('paid', 'Paid'), ('refunded', 'Refunded'), ('cancelled', 'Cancelled')], default='New', max_length=10)),
                ('callback_url', models.CharField(max_length=60, null=True)),
                ('card_details', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='paystuff.carddetails')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_4_card_digits', models.SmallIntegerField()),
                ('type', models.CharField(choices=[('payment', 'Paid'), ('refund', 'Refund')], default='payment', max_length=10)),
                ('currencyCode', models.CharField(max_length=30)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='paystuff.transaction')),
            ],
        ),
    ]