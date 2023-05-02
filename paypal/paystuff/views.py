from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django import forms
from django.core import serializers
from django.shortcuts import get_object_or_404
from .models import *
import json
import random
# Create your views here.

validCodes = ["US", "Pound"]

def validateNewTransaction(transaction):
    fields = [f.name for f in Transaction._meta.get_fields()]
    #fields.remove("payment")
    fields.remove("card_details")
    fields.remove("transaction_id")
    #print("fields", transaction['currencyCode'])
    for field in fields:
        if field not in transaction:
            return field, " not found."

    if transaction['currencyCode'] not in validCodes:
        return "Invalid currency Code"

    return True

def validateBillingAddress(address):
    fields = [f.name for f in BillingAddress._meta.get_fields()]
    print("validateBillingAddressfields", fields)
    if "fullname" in address and "address_1" in address and "address_2" in address and "town_city" in address and "postcode" in address and "region" in address and "country" in address:
        for field in obj:
            if type(obj[field]) != str:
                return field, " is not a string"
        return True
    return "Missing items in billing address."


def validateCardDetails(cardD):
    fields = [f.name for f in CardDetails._meta.get_fields()]
    fields.remove("transaction")
    fields.remove("billingAddress")
    fields.remove("id")
    for field in fields:
        if field not in cardD:
            return field, " not found."
    if len(str(cardD["number"])) == 16:
        return "Invalid length of card number"
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
                deliveryEmail=body['deliveryEmail'],
                deliveryName=body['deliveryName'],
            )
            data = serializers.serialize('json', [transaction,])
            data = addPrimaryKey(json.loads(data)[0])
            return HttpResponse(json.dumps(data))
        else:
            return HttpResponse(validation, status=400)
    else: 
        return HttpResponse('Not a get request', status=400)


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
        return HttpResponse('Not a get request')

@csrf_exempt
def getUserTransactions(request):
    if request.method == 'GET':
        body = json.loads(request.body)
        transactions = Transaction.objects.filter(userId=body["userId"])#.order_by('-date_created')
        data = serializers.serialize('json', transactions)
        transactions = []
        items = json.loads(data)
        for item in items:
            transactions.append(addPrimaryKey(item))
        return HttpResponse(json.dumps(transactions))
    else: 
        return HttpResponse('Not a get request')

@csrf_exempt
def getEmailTransactions(request):
    if request.method == 'GET':
        body = json.loads(request.body)
        try:
            transactions = Transaction.objects.filter(deliveryEmail=body["deliveryEmail"])#.order_by('-date_created')
        except:
            return HttpResponse('Transaction could not be found', status = 404) 

        data = serializers.serialize('json', transactions)
        transactions = []
        items = json.loads(data)
        for item in items:
            transactions.append(addPrimaryKey(item))
        return HttpResponse(json.dumps(transactions))
    else: 
        return HttpResponse('Not a get request')

@csrf_exempt
def makePayment(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        if not ("cardDetails" in body and "billingAddress" in body):
            return HttpResponse('Failed to include all fields.')

        #if not validateBillingAddress(body['billingAddress']):
        if type(validateBillingAddress(body['billingAddress'])) == type(True):
            return HttpResponse(validateBillingAddress(body['billingAddress']))
        elif type(validateCardDetails(body['cardDetails'])) == type(True):
            print("VALIDEAT",validateCardDetails(body['cardDetails']))
            return HttpResponse(validateCardDetails(body['cardDetails']))
        else:
            try:
                transaction = Transaction.objects.get(transaction_id=body["transaction_id"])
            except:
                return HttpResponse('Transaction could not be found', status = 404) 

            if transaction.status != "New":
                return HttpResponse("Payment has already been made.", status=400)

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

            #Update transaction
            transaction.card_details=card
            transaction.status="paid"
            transaction.save()
            data = serializers.serialize('json', [transaction,])
            data = addPrimaryKey(json.loads(data)[0])
            return HttpResponse(json.dumps(data), status=200)
    else: 
        return HttpResponse('Not a post request', status=200)


@csrf_exempt
def refundTransaction(request):
    if request.method == 'GET':
        body = json.loads(request.body)
        try:
            transaction = Transaction.objects.get(transaction_id=body["transaction_id"])
            if transaction.status == "Paid":
                transaction.status = "refunded"
                transaction.save()
                data = serializers.serialize('json', [transaction,])
                struct = json.loads(data)
                data = addPrimaryKey(struct[0])
                return HttpResponse(json.dumps(data))
            else:
                return HttpResponse('Payment could not be refunded', status = 400) 
        except:
            return HttpResponse('Transaction not found', status = 404) 
    else:
        return HttpResponse('This API route only accepts GET requests', status = 400)


@csrf_exempt
def cancelTransaction(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        try:
            transaction = Transaction.objects.get(transaction_id=body["transaction_id"])
            if transaction.status == "New":
                transaction.delete()
                return HttpResponse('Successful deletion', status = 200)
            else:
                return HttpResponse('Payment has already been made or refunded.', status = 400)
        except:
            return HttpResponse('Transaction could not be found', status = 404) 
    else: 
        return HttpResponse('Only post requests allowed', status = 400)  


def makeJson(data):
    fields = data['fields']
    fields['transaction_id'] = data['pk']
    return json.dumps(fields)

def addPrimaryKey(data):
    fields = data['fields']
    cardId = fields['card_details']
    if cardId != None:
        cardDetails = CardDetails.objects.get(id=cardId)
        fields['number'] = str(cardDetails.number)
    fields.pop('card_details')
    fields['transaction_id'] = data['pk']
    return fields
