from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django import forms
from django.core import serializers
from django.shortcuts import get_object_or_404
from .models import *
from django.utils.timezone import *
import datetime
import json
import random
from django.core.mail import send_mail
# Create your views here.

validCodes = ["US", "Pound"]

def validateNewTransaction(transaction):
    fields = [f.name for f in Transaction._meta.get_fields()]
    fields.remove("card_details")
    fields.remove("transaction_id")
    fields.remove("refundAmount")
    fields.remove("updateTime")
    fields.remove("status")
    fields.remove("dateCreated")
    for field in fields:
        if field not in transaction:
            return field, " not found."
    if type(transaction['transactionAmount']) != float:
        return "Amount is not a float"

    if transaction['currencyCode'] not in validCodes:
        return "Invalid currency Code"

    return True

def validateBillingAddress(address):
    fields = [f.name for f in BillingAddress._meta.get_fields()]
    fields.remove("carddetails")
    fields.remove("id")

    for field in fields:
        if field not in address:
            return field, " not found."
    return True


def luhn_checksum(card_number):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = 0
    checksum += sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d*2))
    return checksum % 10

def validateCardDetails(cardD):
    fields = [f.name for f in CardDetails._meta.get_fields()]
    #print("fields", fields)
    fields.remove("transaction")
    fields.remove("billingAddress")
    fields.remove("id")
    fields.remove("user_details")
    #print("VDDDDDDDDDD", fields, cardD)
    for field in fields:
        #print(field)
        if field not in cardD:
            #print("FAILED")
            return field, " not found."
    if len(cardD["number"]) > 16 and len(cardD["number"]) < 20:
        return "Invalid length of card number"
    if luhn_checksum(cardD["number"]):
        return "Invalid Card Test"
    if len(str(cardD["securityCode"])) != 3 and len(str(cardD["securityCode"])) != 4:
        return "Invalid length of security code"
    expiry = cardD["expiryDate"]
    if len(expiry) != 5:
        return "Invalid length of expiry"
    try:
        month = int(expiry[:2])
        year = int(expiry[-2:])
        if month < 0 or month > 12:
            return "Invalid Month"
        if year < 23 or year > 30:
            return "Invalid Year"
    except:
        return "Not a number"
    return True

def addPrimaryKey(data):
    fields = data['fields']
    cardId = fields['card_details']
    if cardId != None:
        cardDetails = CardDetails.objects.get(id=cardId)
        fields['number'] = str(cardDetails.number)
    fields.pop('card_details')
    fields['transaction_id'] = data['pk']
    return fields

def doUser(data):
    fields = data['fields']
    fields['user_id'] = data['pk']
    print("doUser",fields)
    cards = CardDetails.objects.filter(user_details=fields['user_id'])
    fields['card_details'] = dict()
    for i in range(len(cards)):
    #if cardId != None:
        #cardDetails = CardDetails.objects.get(id=cardId)
        #cardDetails = CardDetails.objects.get(id=cardId)
        cardDetails = cards[i]
        cStuff = json.loads(serializers.serialize('json', [cardDetails,]))[0]
        cStuff['fields']['card_id'] = cStuff['pk']
        cStuff = cStuff['fields']

        billingDetails = BillingAddress.objects.get(id=cStuff['billingAddress'])
        bStuff = json.loads(serializers.serialize('json', [billingDetails,]))[0]
        bStuff['fields']['billing_id'] = bStuff['pk']
        bStuff = bStuff['fields']
        cStuff['billingAddress'] = bStuff
        tempS = 'card_details'+ str(i)
        fields['card_details'][str(i)] = cStuff
    return fields

    




@csrf_exempt
def createTransaction(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        #header = json.loads(request.header)
        validation = validateNewTransaction(body)
        if type(validation) == type(True):
            transaction = Transaction.objects.create(userId=body['userId'],
                orderId=body['orderId'],
                merchantId=body['merchantId'], 
                transactionAmount=body['transactionAmount'],
                currencyCode=body['currencyCode'],
                dateCreated= now(),
                updateTime= now(),
                deliveryEmail=body['deliveryEmail'],
                deliveryName=body['deliveryName'],
            )
            data = serializers.serialize('json', [transaction,])
            data = addPrimaryKey(json.loads(data)[0])
            return HttpResponse(json.dumps(data))
        else:
            return HttpResponse(validation, status=400)
    else: 
        return HttpResponse('Only post requests allowed', status=400)


@csrf_exempt
def getTransaction(request):
    if request.method == 'GET':
        try:
            body = json.loads(request.body)
            transaction = Transaction.objects.get(transaction_id=body["transaction_id"])
            data = serializers.serialize('json', [transaction,])
            data = addPrimaryKey(json.loads(data)[0])
            return HttpResponse(json.dumps(data))
        except:
            return HttpResponse('Transaction could not be found', status = 404) 
    else: 
        return HttpResponse('Only get requests allowed', status=400)

@csrf_exempt
def getUserTransactions(request):
    if request.method == 'GET':
        body = json.loads(request.body)
        transactions = Transaction.objects.filter(userId=body["userId"])
        data = serializers.serialize('json', transactions)
        transactions = []
        items = json.loads(data)
        for item in items:
            transactions.append(addPrimaryKey(item))
        return HttpResponse(json.dumps(transactions))
    else: 
        return HttpResponse('Only get requests allowed', status=400)

@csrf_exempt
def getUserDetails(request):
    if request.method == 'GET':
        body = json.loads(request.body)
        print("body", body)
        try:
            user = User.objects.get(email=body["email"], password=body["password"])
        except:
            return HttpResponse('Invalid User', status = 400) 

        return HttpResponse(json.dumps(doUser(json.loads(serializers.serialize('json', [user,]))[0])))
    else: 
        return HttpResponse('Only get requests allowed', status=400)

@csrf_exempt
def getEmailTransactions(request):
    if request.method == 'GET':
        body = json.loads(request.body)
        try:
            transactions = Transaction.objects.filter(deliveryEmail=body["deliveryEmail"])
        except:
            return HttpResponse('Transaction could not be found', status = 404) 

        data = serializers.serialize('json', transactions)
        transactions = []
        items = json.loads(data)
        for item in items:
            transactions.append(addPrimaryKey(item))
        return HttpResponse(json.dumps(transactions))
    else: 
        return HttpResponse('Only get requests allowed')

@csrf_exempt
def makePayment(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        if not ("cardDetails" in body and "billingAddress" in body):
            return HttpResponse('Failed to include all fields.')

        if type(validateBillingAddress(body['billingAddress'])) != type(True):
            return HttpResponse(validateBillingAddress(body['billingAddress']), status=400)
        elif type(validateCardDetails(body['cardDetails'])) != type(True):
            return HttpResponse(validateCardDetails(body['cardDetails']), status=400)
        else:
            try:
                transaction = Transaction.objects.get(transaction_id=body["transaction_id"])
            except:
                return HttpResponse('Transaction could not be found', status = 404) 

            if transaction.status != "Unpaid":
                return HttpResponse("Payment has already been made.", status=400)

            if (transaction.userId == "-1"):
                #Save billing and card details
                billing = BillingAddress.objects.create(name=body['billingAddress']['name'],
                    addressLine1=body['billingAddress']['addressLine1'],
                    addressLine2=body['billingAddress']['addressLine2'],
                    city=body['billingAddress']['city'],
                    postcode=body['billingAddress']['postcode'],
                    region=body['billingAddress']['region'],
                    countryCode=body['billingAddress']['countryCode'])

                card = CardDetails.objects.create(number=body['cardDetails']['number'],
                    securityCode=body['cardDetails']['securityCode'],
                    expiryDate=body['cardDetails']['expiryDate'],
                    billingAddress=billing)
            else:
                billing = BillingAddress.objects.get(id=body['billingAddress']['billing_id'])
                card = CardDetails.objects.get(id=body['cardDetails']['card_id'])

            #Update transaction
            transaction.card_details=card
            transaction.status="paid"
            transaction.save()
            data = serializers.serialize('json', [transaction,])
            data = addPrimaryKey(json.loads(data)[0])
            return HttpResponse(json.dumps(data), status=200)
    else: 
        return HttpResponse('Only post requests allowed', status=400)


@csrf_exempt
def refundTransaction(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        try:
            transaction = Transaction.objects.get(transaction_id=body["transaction_id"])
        except:
            return HttpResponse('Transaction not found', status = 404) 
        #print("refundtransaction.status", transaction.status)
        if type(body['refundAmount']) != float:
            return "Amount is not a float"
        if transaction.status == "Paid" or transaction.status == "paid":
            transaction.status = "Refunded"
            transaction.refundAmount = body["refundAmount"]
            transaction.dateUpdated = now()
            transaction.save()
            data = serializers.serialize('json', [transaction,])
            data = addPrimaryKey(json.loads(data)[0])
            return HttpResponse(json.dumps(data))
        else:
            return HttpResponse('Payment could not be refunded', status = 400) 
    else:
        return HttpResponse('Only post requests allowed', status = 400)


@csrf_exempt
def cancelTransaction(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        try:
            transaction = Transaction.objects.get(transaction_id=body["transaction_id"])
        except:
            return HttpResponse('Transaction could not be found', status = 404) 
        if transaction.status == "Unpaid":
            transaction.delete()
            return HttpResponse('Successful deletion', status = 200)
        else:
            return HttpResponse('Payment has already been made or refunded.', status = 400)
    else: 
        return HttpResponse('Only post requests allowed', status = 400)  

