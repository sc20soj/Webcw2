# Generated by Django 4.1.7 on 2023-04-30 18:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paystuff', '0003_remove_payment_last_4_card_digits_payment_cardnumber_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Payment',
        ),
    ]
