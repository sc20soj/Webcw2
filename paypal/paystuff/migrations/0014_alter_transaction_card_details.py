# Generated by Django 4.1.7 on 2023-05-05 12:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('paystuff', '0013_remove_transaction_callback_url_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='card_details',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='paystuff.carddetails'),
        ),
    ]