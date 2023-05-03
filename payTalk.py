import requests



def payTalk(transactionDetails):
    choice = input("Press 1 for user login, 2 for guest, other to cancel")
    if ("1" == choice):
        while True:
            email = input("Enter email")
            password = input("Enter email")
            data = '{"email": "sc20soj@leeds.ac.uk", "password":"James"}'
            response = requests.get('http://127.0.0.1:8000/api/getUserDetails', headers=transactionHeaders, data=data)
            if(response.status_code == 200):
                response = requests.post('http://127.0.0.1:8000/api/makePayment', headers=transactionHeaders, data=data)
                if(response.status_code == 200):
                    print("Successful",response.text)
                else: # Shouldn't reach this under any circumstance
                    print("Error: ",response.text)
            else:
                print("Error: ",response.text)

    elif ("2" == choice):
        email = input("Enter email")
        deliveryName = input("Enter name")
        response = requests.post('http://127.0.0.1:8000/api/createTransaction/', headers=transactionHeaders, data=data)
        if(response.status_code == 200):
                response = requests.post('http://127.0.0.1:8000/api/makePayment', headers=transactionHeaders, data=data)
                if(response.status_code == 200):
                    print("Successful",response.text)
                else: # Shouldn't reach this under any circumstance
                    print("Error: ",response.text)
            else:
                print("Error: ",response.text)

    else:




class BillingAddress(models.Model):
    name = models.CharField(max_length=30)
    addressLine1 = models.CharField(max_length=30)
    addressLine2 = models.CharField(max_length=30)
    city = models.CharField(max_length=20)
    postcode = models.CharField(max_length=10)
    region = models.CharField(max_length=20)
    countryCode = models.CharField(max_length=20)


class CardDetails(models.Model):
    number = models.CharField(max_length=19, null=True)
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
    dateCreated = models.DateTimeField(auto_now_add=False)

    status_choices = [("unpaid", "Unpaid"), ("paid", "Paid"), ("refunded", "Refunded")]
    status = models.CharField(max_length=10, choices=status_choices, default="Unpaid")

    refundAmount = models.DecimalField(decimal_places=2, max_digits=8, default=0)
    updateTime = models.DateTimeField(auto_now_add=False)

    card_details = models.ForeignKey(CardDetails, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return u'Transaction ID: %s User ID: %s' % (self.transaction_id, self.userId)
    def get_fields():
        return self._meta.fields


class User(models.Model):
    user_id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    card_details = models.ForeignKey(CardDetails, on_delete=models.PROTECT, null=True)
