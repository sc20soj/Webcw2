# Generated by Django 4.1.7 on 2023-05-03 12:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('paystuff', '0010_alter_transaction_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=30)),
                ('cards', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='paystuff.carddetails')),
            ],
        ),
    ]
