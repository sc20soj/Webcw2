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


    def test_getUserDetails(self):
        #if "userId" not in obj or "orderId" not in obj or "merchantId" not in obj or "deliveryEmail" not in obj or "deliveryName" not in obj or "transactionAmount" not in obj
        data = '{"email": "sc20soj@leeds.ac.uk", "password":"James"}'
        response = requests.get('http://127.0.0.1:8000/api/getUserDetails', headers=self.transactionHeaders, data=data)
        print("test_getUserDetails ",response.text)
        self.assertTrue(response.status_code == 200)


    def test_get_refundTransaction(self):
        data = '{"transaction_id": "7", "refundAmount": 20.00}'
        response = requests.post('http://127.0.0.1:8000/api/refundTransaction', headers=self.transactionHeaders, data=data)
        print("test_get_refundTransaction ",response.text)
        self.assertTrue(response.status_code == 200)


    def test_make_payment(self):
        #if "userId" not in obj or "orderId" not in obj or "merchantId" not in obj or "deliveryEmail" not in obj or "deliveryName" not in obj or "transactionAmount" not in obj
        data = '{"transaction_id": "7", "cardDetails" :{"number":"4929340575740113", "securityCode":"123", "expiryDate":"03/27"}, "billingAddress" : {"name":"scott", "addressLine1":"33 Windsor", "addressLine2":"33 Windsor", "city":"southport", "postcode":"PE6 5SU","region":"MerseySide", "countryCode":"uk"} }'
        response = requests.post('http://127.0.0.1:8000/api/makePayment', headers=self.transactionHeaders, data=data)
        print("test_make_payment ",response.text)
        self.assertTrue(response.status_code == 200)

    def test_wrong_payment(self):
        #if "userId" not in obj or "orderId" not in obj or "merchantId" not in obj or "deliveryEmail" not in obj or "deliveryName" not in obj or "transactionAmount" not in obj
        data = '{"transaction_id": "7", "cardDetails" :{"securityCode":"123", "expiryDate":"03/27"}, "billingAddress" : {"name":"scott", "addressLine1":"33 Windsor", "addressLine2":"33 Windsor", "city":"southport", "postcode":"PE6 5SU","region":"MerseySide", "countryCode":"uk"} }'
        response = requests.post('http://127.0.0.1:8000/api/makePayment', headers=self.transactionHeaders, data=data)
        print("test_wrong_payment ",response.text)
        self.assertTrue(response.status_code == 400)

    def test_create_transaction(self):
        #if "userId" not in obj or "orderId" not in obj or "merchantId" not in obj or "deliveryEmail" not in obj or "deliveryName" not in obj or "transactionAmount" not in obj
        #data = '{ "userId": "-1", "orderId": "1", "merchantId": "1", "currencyCode": "US", "transactionAmount": "60.35", "deliveryEmail": "sj@l.ac.uk", "deliveryName": "Scott"}'data = '{ "userId": "-1", "orderId": "1", "merchantId": "1", "currencyCode": "US", "transactionAmount": "60.35", "deliveryEmail": "sj@l.ac.uk", "deliveryName": "Scott", "dateCreated": "27/03/2002", "dateCreated": "27/03/2002","status": "new","callback_url": "scott.co.uk"}'
        data = '{ "userId": "-1", "orderId": "1", "merchantId": "1", "currencyCode": "US", "transactionAmount": 60.35, "deliveryEmail": "sj@l.ac.uk", "deliveryName": "Scott"}'
        response = requests.post('http://127.0.0.1:8000/api/createTransaction/', headers=self.transactionHeaders, data=data)
        print("test_make_transaction ",response.text)
        self.assertTrue(response.status_code == 200)

    def test_transaction_field_checker(self):
        data = '{"dateCreated": "27/03/2002", "status": "new"}'
        response = requests.post('http://127.0.0.1:8000/api/createTransaction/', headers=self.transactionHeaders, data=data)
        print("test_transaction_field_checker ",response.text)
        self.assertTrue(response.status_code == 400)


    def test_get_transaction(self):
        data = '{"transaction_id": "1"}'
        response = requests.get('http://127.0.0.1:8000/api/getTransaction', headers=self.transactionHeaders, data=data)
        print("test_get_transaction_checker ",response.text)
        self.assertTrue(response.status_code == 200)
    

    def test_get_user_transactions(self):
        data = '{"userId": "1"}'
        response = requests.get('http://127.0.0.1:8000/api/getUserTransactions', headers=self.transactionHeaders, data=data)
        #print("test_get_user_transactions ",response.text)
        self.assertTrue(response.status_code == 200)

    def test_get_email_transactions(self):
        data = '{"deliveryEmail": "sc20soj@leeds.ac.uk"}'
        response = requests.get('http://127.0.0.1:8000/api/getEmailTransactions', headers=self.transactionHeaders, data=data)
        print("test_get_email_transactions ",response.text)
        self.assertTrue(response.status_code == 200)


    #def test_make_payment(self):
    #    #if "userId" not in obj or "orderId" not in obj or "merchantId" not in obj or "deliveryEmail" not in obj or "deliveryName" not in obj or "transactionAmount" not in obj
    #    #data = '{"cardDetails" :{"number":"1234567890123456", "securityCode":"123", "expiryDate":"03/27"}, "billingAddress" : {"name":"scott", "addressLine1":"33 Windsor", "addressLine2":"33 Windsor", "city":"southport", "postcode":"PE6 5SU","region":"MerseySide", "countryCode":"uk"} }'
    #    response = requests.post('http://127.0.0.1:8000/api/deleteTransaction/18', headers=self.transactionHeaders)
    #    print("test_make_payment ",response.text)
    #    self.assertTrue(response.status_code == 200)

