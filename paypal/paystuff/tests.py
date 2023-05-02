from django.test import TestCase
import requests
from .models import *

# Create your tests here.

class YourTestClass(TestCase):
    def setUp(self):
        
        self.transactionHeaders = {
            'Content-Type': 'application/json',
            'PayPal-Request-Id': '7b92603e-77ed-4896-8e78-5dea2050476a',
            'Authorization': 'Bearer 6V7rbVwmlM1gFZKW_8QtzWXqpcwQ6T5vhEGYNJDAAdn3paCgRpdeMdVYmWzgbKSsECednupJ3Zx5Xd-g',
        }

        Transaction.objects.all().delete()

    def tearDown(self):
        entries= Transaction.objects.all()
        entries.delete()

    def test_make_transaction(self):
        #if "userId" not in obj or "orderId" not in obj or "merchantId" not in obj or "deliveryEmail" not in obj or "deliveryName" not in obj or "transactionAmount" not in obj
        data = '{ "userId": "1", "orderId": "1", "merchantId": "1", "currencyCode": "US", "transactionAmount": "60.35", "deliveryEmail": "sj@l.ac.uk", "deliveryName": "Scott", "dateCreated": "27/03/2002", "dateCreated": "27/03/2002","status": "new","callback_url": "scott.co.uk"}'
        response = requests.post('http://127.0.0.1:8000/api/createTransaction/', headers=self.transactionHeaders, data=data)
        #print("test_make_transaction ",response.text)
        self.assertTrue(response.status_code == 200)

    def test_transaction_field_checker(self):
        data = '{"dateCreated": "27/03/2002", "status": "new"}'
        response = requests.post('http://127.0.0.1:8000/api/createTransaction/', headers=self.transactionHeaders, data=data)
        #print("test_transaction_field_checker ",response.text)
        self.assertTrue(response.status_code == 400)

    def test_get_transaction(self):
        data = '{"transaction_id": "24"}'
        response = requests.get('http://127.0.0.1:8000/api/getTransaction', headers=self.transactionHeaders, data=data)
        #print("test_get_transaction_checker ",response.text)
        self.assertTrue(response.status_code == 200)

    """
    def test_get_user_transactions(self):
        data = '{"doesntMatter": "ninjas"}'
        response = requests.get('http://127.0.0.1:8000/api/getUserTransactions/1', headers=self.transactionHeaders, data=data)
        #print("test_get_user_transactions ",response.text)
        self.assertTrue(response.status_code == 200)
"""
    def test_make_payment(self):
        #if "userId" not in obj or "orderId" not in obj or "merchantId" not in obj or "deliveryEmail" not in obj or "deliveryName" not in obj or "transactionAmount" not in obj
        data = '{"transaction_id": "27", "cardDetails" :{"number":"1234567890123456", "securityCode":"123", "expiryDate":"03/27"}, "billingAddress" : {"name":"scott", "addressLine1":"33 Windsor", "addressLine2":"33 Windsor", "city":"southport", "postcode":"PE6 5SU","region":"MerseySide", "countryCode":"uk"} }'
        response = requests.post('http://127.0.0.1:8000/api/makePayment', headers=self.transactionHeaders, data=data)
        print("test_make_payment ",response.text)
        self.assertTrue(response.status_code == 200)

    #def test_make_payment(self):
    #    #if "userId" not in obj or "orderId" not in obj or "merchantId" not in obj or "deliveryEmail" not in obj or "deliveryName" not in obj or "transactionAmount" not in obj
    #    #data = '{"cardDetails" :{"number":"1234567890123456", "securityCode":"123", "expiryDate":"03/27"}, "billingAddress" : {"name":"scott", "addressLine1":"33 Windsor", "addressLine2":"33 Windsor", "city":"southport", "postcode":"PE6 5SU","region":"MerseySide", "countryCode":"uk"} }'
    #    response = requests.post('http://127.0.0.1:8000/api/deleteTransaction/18', headers=self.transactionHeaders)
    #    print("test_make_payment ",response.text)
    #    self.assertTrue(response.status_code == 200)


"""
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
    #number = models.BigIntegerField()
    securityCode = models.CharField(max_length=4, null=True)
    expiryDate = models.CharField(max_length=7)

    #cvv = models.SmallIntegerField()
    #expiryDate = models.CharField(max_length=5)
    billingAddress = models.ForeignKey(BillingAddress, on_delete=models.PROTECT)




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
"""