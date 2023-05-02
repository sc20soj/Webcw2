from django.db import models

# Create your models here.


class BillingAddress(models.Model):
    name = models.CharField(max_length=30)
    addressLine1 = models.CharField(max_length=30)
    addressLine2 = models.CharField(max_length=30)
    city = models.CharField(max_length=20)
    postcode = models.CharField(max_length=10)
    region = models.CharField(max_length=20)
    countryCode = models.CharField(max_length=20)


class CardDetails(models.Model):
    number = models.CharField(max_length=16, null=True)
    securityCode = models.CharField(max_length=4, null=True)
    expiryDate = models.CharField(max_length=5)
    billingAddress = models.ForeignKey(BillingAddress, on_delete=models.PROTECT)


class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True, editable=False)
    orderId = models.CharField(max_length=30)
    userId = models.CharField(max_length=30)
    merchantId = models.CharField(max_length=30)

    currencyCode = models.CharField(max_length=30)
    transactionAmount = models.DecimalField(decimal_places=2, max_digits=8)
    deliveryEmail = models.CharField(max_length=30)
    deliveryName = models.CharField(max_length=30)
    dateCreated = models.DateField(auto_now_add=True)

    status_choices = [("new", "New"), ("paid", "Paid"), ("refunded", "Refunded"), ("cancelled", "Cancelled")]
    status = models.CharField(max_length=10, choices=status_choices, default="New")

    callback_url = models.CharField(max_length=60, null=True)
    card_details = models.ForeignKey(CardDetails, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return u'Transaction ID: %s User ID: %s' % (self.transaction_id, self.userId)
    def get_fields():
        return self._meta.fields

"""
class User(models.Model):
    firstName = models.CharField(max_length=30)
    secondName = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    cards = models.ForeignKey(CardDetails, on_delete=models.PROTECT, null=True)
"""